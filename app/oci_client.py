import oci
from oci.identity import IdentityClient
from oci.core import VirtualNetworkClient, ComputeClient
from app.oci_config import get_configuration, get_compartment_scope, get_vcn_scope

config = get_configuration()
identity_client = IdentityClient(config)
compute_client = ComputeClient(config)
network_client = VirtualNetworkClient(config)


def get_oci_user():
    user = identity_client.get_user(config["user"]).data
    return user


def get_compute_instances_details():

    try:
        response = compute_client.list_instances(compartment_id=get_compartment_scope())
        return response.data
    except Exception as e:
        return {"problem encountered": e.__repr__()}


def get_compute_instances_status():

    try:
        response = {}
        instance_responses = compute_client.list_instances(compartment_id=get_compartment_scope())
        for i in instance_responses.data:
            response[i.display_name] = {'display_name': i.display_name,
                                        'lifecycle_state': i.lifecycle_state,
                                        'id': i.id}

        return response
    except Exception as e:
        return {"problem encountered": e.__repr__()}


def stop_all_compute_instances(soft_stop=True):

    try:
        instance_responses = compute_client.list_instances(compartment_id=get_compartment_scope())

        response = {}
        actions = {}

        response['stopping'] = actions

        # for every instance sent stop command
        for i in instance_responses.data:

            if i.lifecycle_state == 'RUNNING':

                if soft_stop:
                    compute_client.instance_action(i.id, 'SOFTSTOP')
                    print('SOFT stopping instance {} ', i.id)

                else:
                    compute_client.instance_action(i.id, 'STOP')
                    print('HARD stopping instance {} ', i.id)

                actions[i.display_name] = {i.display_name: i.id}

        return response

    except Exception as e:
        return {"problem encountered": e.__repr__()}


def start_all_compute_instances():

    try:
        instance_responses = compute_client.list_instances(compartment_id=get_compartment_scope())

        response = {}
        # for every instance sent stop command
        for i in instance_responses.data:
            if i.lifecycle_state == 'STOPPED':
                compute_client.instance_action(i.id, 'START')
                response['starting'] = {i.display_name: i.id}

        return response

    except Exception as e:
        return {"problem encountered": e.__repr__()}


# def get_public_ip(ip_address):
#
#     get_public_ip_by_ip_address_response = network_client.get_public_ip_by_ip_address(
#         get_public_ip_by_ip_address_details=oci.core.models.GetPublicIpByIpAddressDetails(
#             ip_address=ip_address))
#
#     return get_public_ip_by_ip_address_response


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


def get_vcn_topology():

    try:
        response = network_client.get_vcn_topology(
            compartment_id=get_compartment_scope(),
            vcn_id=get_vcn_scope())

            # access_level="ANY",
            # query_compartment_subtree=True,
            # if_none_match="Nothing-Matched")

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
        instance_list = get_compute_instances_details()
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

