import oci
from oci.identity import IdentityClient
from oci.core import VirtualNetworkClient, ComputeClient
from app.oci_config import get_configuration, get_compartment_scope

config = get_configuration()
identity_client = IdentityClient(config)
compute_client = ComputeClient(config)
network_client = VirtualNetworkClient(config)


def get_oci_user():
    user = identity_client.get_user(config["user"]).data
    return user


def get_compute_instances():

    try:
        response = compute_client.list_instances(compartment_id=get_compartment_scope())
        return response.data
    except Exception as e:
        return {"problem encountered": e.__repr__()}


def get_vnic_attachments():

    try:
        response = compute_client.list_vnic_attachments(compartment_id=get_compartment_scope())
        return response.data
    except Exception as e:
        return {"problem encountered": e.__repr__()}


def get_vcns():

    try:
        response = network_client.list_vcns(compartment_id=get_compartment_scope())
        return response.data
    except Exception as e:
        return {"problem encountered": e.__repr__()}


def get_subnets():

    try:
        response = network_client.list_subnets(compartment_id=get_compartment_scope())
        return response.data
    except Exception as e:
        return {"problem encountered": e.__repr__()}


def vcn_with_attached_compute():

    try:

        vcn_map = {}
        subnet_map = {}
        instance_map = {}
        attach_map = {}
        result_map = {}

        vcn_list = get_vcns()
        subnet_list = get_subnets()
        instance_list = get_compute_instances()
        attach_list = get_vnic_attachments()

        for vcn in vcn_list:
            vcn_id = vcn.id
            vcn_map[vcn_id] = vcn

        for subnet in subnet_list:
            subnet_id = subnet.id
            subnet_map[subnet_id] = subnet

        for attach in attach_list:
            attach_id = attach.id
            attach_map[attach_id] = attach

        for instance in instance_list:
            instance_id = instance.id
            instance_map[instance_id] = instance

        for attachment in attach_map.values():

            subnet = subnet_map.get(attachment.subnet_id)
            instance = instance_map.get(attachment.instance_id)
            vcn_digest = result_map.get(subnet.vcn_id)

            if vcn_digest is None:
                vcn = vcn_map.get(subnet.vcn_id)
                vcn_digest = {'vcn_id': vcn.id,
                              'vcn_display_name': vcn.display_name,
                              'vcn_compartment_id': vcn.compartment_id,
                              'vcn_vnic_attached_instances': list()}

                result_map[vcn.id] = vcn_digest

            instance_digest = {'vnic_id': attachment.vnic_id,
                               'vnic_attachment_id': attachment.id,
                               'instance_id': instance.id,
                               'instance_display_name': instance.display_name,
                               'instance_compartment_id': instance.compartment_id,
                               'subnet_id': subnet.id,
                               'subnet_display_name': subnet.display_name,
                               'subnet_compartment_id': subnet.compartment_id}

            vcn_digest['vcn_vnic_attached_instances'].append(instance_digest)

        return result_map

    except oci.exceptions.RequestException as e:
        return {"RequestException": e.__repr__()}

    except oci.exceptions.ServiceError as e:
        return {"ServiceError": e.__repr__()}

    except Exception as e:
        return {"problem encountered": e.__repr__()}



