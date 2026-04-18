# Creates the Virtual Cloud Network (VCN)
resource "oci_core_vcn" "free_vcn" {
  cidr_block     = "10.0.0.0/16"
  compartment_id = var.compartment_ocid
  display_name   = "mcp-free-vcn"
}

resource "oci_core_subnet" "free_subnet" {
  cidr_block        = "10.0.1.0/24"
  display_name      = "mcp-free-subnet"
  compartment_id    = var.compartment_ocid
  vcn_id            = oci_core_vcn.free_vcn.id
  route_table_id    = oci_core_vcn.free_vcn.default_route_table_id
  security_list_ids = [oci_core_vcn.free_vcn.default_security_list_id]
}

# The Always Free ARM Ampere A1 Compute Instances (Up to 4 OCPUs and 24GB RAM free!)
resource "oci_core_instance" "k3s_server" {
  availability_domain = data.oci_identity_availability_domains.ads.availability_domains[0].name
  compartment_id      = var.compartment_ocid
  shape               = "VM.Standard.A1.Flex" # Always Free ARM Shape
  display_name        = "mcp-k3s-master"

  shape_config {
    ocpus         = 2  # Utilizing half the free tier limit
    memory_in_gbs = 12 # Utilizing half the free tier limit
  }

  create_vnic_details {
    subnet_id        = oci_core_subnet.free_subnet.id
    assign_public_ip = true
  }

  source_details {
    source_type = "image"
    source_id   = var.ubuntu_arm_image_ocid
  }

  metadata = {
    ssh_authorized_keys = var.ssh_public_key
    # Inject user-data to automatically install K3s on boot!
    user_data = base64encode(<<-EOF
      #!/bin/bash
      curl -sfL https://get.k3s.io | sh -
    EOF
    )
  }
}

data "oci_identity_availability_domains" "ads" {
  compartment_id = var.tenancy_ocid
}

variable "ubuntu_arm_image_ocid" {
  description = "OCID for Ubuntu 22.04 ARM"
}
variable "ssh_public_key" {}
