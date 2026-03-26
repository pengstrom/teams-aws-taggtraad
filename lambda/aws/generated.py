"""Pydantic models for AWS API Call via CloudTrail EventBridge events (aws.ec2)."""

from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


# --- Leaf / near-leaf models ---


class Attributes(BaseModel):
    mfa_authenticated: Optional[str] = Field(None, alias="mfaAuthenticated")
    creation_date: Optional[datetime] = Field(None, alias="creationDate")


class SessionIssuer(BaseModel):
    account_id: Optional[str] = Field(None, alias="accountId")
    principal_id: Optional[str] = Field(None, alias="principalId")
    type: Optional[str] = None
    arn: Optional[str] = None
    user_name: Optional[str] = Field(None, alias="userName")


class SessionContext(BaseModel):
    web_id_federation_data: Optional[dict] = Field(None, alias="webIdFederationData")
    session_issuer: Optional[SessionIssuer] = Field(None, alias="sessionIssuer")
    attributes: Optional[Attributes] = None


class UserIdentity(BaseModel):
    session_context: Optional[SessionContext] = Field(None, alias="sessionContext")
    access_key_id: Optional[str] = Field(None, alias="accessKeyId")
    account_id: str = Field(..., alias="accountId")
    principal_id: str = Field(..., alias="principalId")
    type: str
    arn: str
    invoked_by: Optional[str] = Field(None, alias="invokedBy")


# --- Instance / ENI primitives ---


class InstanceState(BaseModel):
    code: Optional[float] = None
    name: Optional[str] = None


class StateReason(BaseModel):
    code: Optional[str] = None
    message: Optional[str] = None


class CapacityReservationSpecification(BaseModel):
    capacity_reservation_preference: Optional[str] = Field(
        None, alias="capacityReservationPreference"
    )


class CpuOptions(BaseModel):
    threads_per_core: Optional[float] = Field(None, alias="threadsPerCore")
    core_count: Optional[float] = Field(None, alias="coreCount")


class Monitoring1(BaseModel):
    state: Optional[str] = None


class EnclaveOptions(BaseModel):
    enabled: Optional[bool] = None


class Placement(BaseModel):
    tenancy: Optional[str] = None
    availability_zone: Optional[str] = Field(None, alias="availabilityZone")


class GroupSet2Item(BaseModel):
    group_name: Optional[str] = Field(None, alias="groupName")
    group_id: Optional[str] = Field(None, alias="groupId")


class GroupSet2(BaseModel):
    items: Optional[list[GroupSet2Item]] = None


class PrivateIpAddressesSetItem(BaseModel):
    private_ip_address: Optional[str] = Field(None, alias="privateIpAddress")
    primary: Optional[bool] = None


class PrivateIpAddressesSet1(BaseModel):
    item: Optional[list[PrivateIpAddressesSetItem]] = None


class PrivateIpAddressesSet2(BaseModel):
    item: list[PrivateIpAddressesSetItem]


class Attachment(BaseModel):
    attachment_id: Optional[str] = Field(None, alias="attachmentId")
    delete_on_termination: Optional[bool] = Field(None, alias="deleteOnTermination")
    device_index: Optional[float] = Field(None, alias="deviceIndex")
    attach_time: Optional[int] = Field(None, alias="attachTime")
    status: Optional[str] = None


class GroupSet3(BaseModel):
    items: list[GroupSet2Item]


class NetworkInterfaceSet1Item(BaseModel):
    group_set: Optional[GroupSet3] = Field(None, alias="groupSet")
    tag_set: Optional[dict] = Field(None, alias="tagSet")
    attachment: Optional[Attachment] = None
    ipv6_addresses_set: Optional[dict] = Field(None, alias="ipv6AddressesSet")
    private_ip_addresses_set: Optional[PrivateIpAddressesSet2] = Field(
        None, alias="privateIpAddressesSet"
    )
    network_interface_id: Optional[str] = Field(None, alias="networkInterfaceId")
    subnet_id: Optional[str] = Field(None, alias="subnetId")
    owner_id: Optional[str] = Field(None, alias="ownerId")
    source_dest_check: Optional[bool] = Field(None, alias="sourceDestCheck")
    private_ip_address: Optional[str] = Field(None, alias="privateIpAddress")
    interface_type: Optional[str] = Field(None, alias="interfaceType")
    mac_address: Optional[str] = Field(None, alias="macAddress")
    vpc_id: Optional[str] = Field(None, alias="vpcId")
    status: Optional[str] = None


class NetworkInterfaceSet1(BaseModel):
    items: Optional[list[NetworkInterfaceSet1Item]] = None


class TagItem(BaseModel):
    value: Optional[str] = None
    key: Optional[str] = None


class TagSet(BaseModel):
    items: Optional[list[TagItem]] = None


class InstancesSetItem(BaseModel):
    """Single instance in a RunInstances / TerminateInstances response."""

    capacity_reservation_specification: Optional[CapacityReservationSpecification] = (
        Field(None, alias="capacityReservationSpecification")
    )
    state_reason: Optional[StateReason] = Field(None, alias="stateReason")
    group_set: Optional[GroupSet2] = Field(None, alias="groupSet")
    tag_set: Optional[TagSet] = Field(None, alias="tagSet")
    instance_state: Optional[InstanceState] = Field(None, alias="instanceState")
    product_codes: Optional[dict] = Field(None, alias="productCodes")
    network_interface_set: Optional[NetworkInterfaceSet1] = Field(
        None, alias="networkInterfaceSet"
    )
    block_device_mapping: Optional[dict] = Field(None, alias="blockDeviceMapping")
    cpu_options: Optional[CpuOptions] = Field(None, alias="cpuOptions")
    monitoring: Optional[Monitoring1] = None
    previous_state: Optional[InstanceState] = Field(None, alias="previousState")
    enclave_options: Optional[EnclaveOptions] = Field(None, alias="enclaveOptions")
    placement: Optional[Placement] = None
    current_state: Optional[InstanceState] = Field(None, alias="currentState")
    subnet_id: Optional[str] = Field(None, alias="subnetId")
    virtualization_type: Optional[str] = Field(None, alias="virtualizationType")
    ami_launch_index: Optional[float] = Field(None, alias="amiLaunchIndex")
    source_dest_check: Optional[bool] = Field(None, alias="sourceDestCheck")
    instance_id: Optional[str] = Field(None, alias="instanceId")
    vpc_id: Optional[str] = Field(None, alias="vpcId")
    hypervisor: Optional[str] = None
    root_device_name: Optional[str] = Field(None, alias="rootDeviceName")
    architecture: Optional[str] = None
    ebs_optimized: Optional[bool] = Field(None, alias="ebsOptimized")
    image_id: Optional[str] = Field(None, alias="imageId")
    client_token: Optional[str] = Field(None, alias="clientToken")
    instance_type: Optional[str] = Field(None, alias="instanceType")
    private_ip_address: Optional[str] = Field(None, alias="privateIpAddress")
    instance_lifecycle: Optional[str] = Field(None, alias="instanceLifecycle")
    root_device_type: Optional[str] = Field(None, alias="rootDeviceType")
    launch_time: Optional[int] = Field(None, alias="launchTime")
    spot_instance_request_id: Optional[str] = Field(None, alias="spotInstanceRequestId")


class InstancesSet(BaseModel):
    items: Optional[list[InstancesSetItem]] = None


# --- Launch template models ---


class LaunchTemplate1(BaseModel):
    create_time: Optional[datetime] = Field(None, alias="createTime")
    created_by: Optional[str] = Field(None, alias="createdBy")
    launch_template_id: Optional[str] = Field(None, alias="launchTemplateId")
    latest_version_number: Optional[float] = Field(None, alias="latestVersionNumber")
    default_version_number: Optional[float] = Field(None, alias="defaultVersionNumber")
    launch_template_name: Optional[str] = Field(None, alias="launchTemplateName")


class SpotOptions2(BaseModel):
    spot_instance_type: Optional[str] = Field(None, alias="SpotInstanceType")
    max_price: Optional[float] = Field(None, alias="MaxPrice")


class InstanceMarketOptions1(BaseModel):
    spot_options: Optional[SpotOptions2] = Field(None, alias="SpotOptions")
    market_type: Optional[str] = Field(None, alias="MarketType")


class SecurityGroupId(BaseModel):
    tag: Optional[float] = None
    content: Optional[str] = None


class NetworkInterface1(BaseModel):
    security_group_id: Optional[SecurityGroupId] = Field(None, alias="SecurityGroupId")
    device_index: Optional[float] = Field(None, alias="DeviceIndex")
    tag: Optional[float] = None
    subnet_id: Optional[str] = Field(None, alias="SubnetId")


class LaunchTemplateData(BaseModel):
    instance_market_options: Optional[InstanceMarketOptions1] = Field(
        None, alias="InstanceMarketOptions"
    )
    network_interface: Optional[NetworkInterface1] = Field(
        None, alias="NetworkInterface"
    )
    user_data: Optional[str] = Field(None, alias="UserData")
    image_id: Optional[str] = Field(None, alias="ImageId")
    instance_type: Optional[str] = Field(None, alias="InstanceType")


class CreateLaunchTemplateRequest(BaseModel):
    launch_template_data: Optional[LaunchTemplateData] = Field(
        None, alias="LaunchTemplateData"
    )
    launch_template_name: Optional[str] = Field(None, alias="LaunchTemplateName")


class DeleteLaunchTemplateRequest(BaseModel):
    launch_template_name: Optional[str] = Field(None, alias="LaunchTemplateName")


class DeleteLaunchTemplateResponse(BaseModel):
    launch_template: Optional[LaunchTemplate1] = Field(None, alias="launchTemplate")
    xmlns: Optional[str] = None
    request_id: Optional[str] = Field(None, alias="requestId")


# --- Fleet models ---


class TargetCapacitySpecification(BaseModel):
    default_target_capacity_type: Optional[str] = Field(
        None, alias="DefaultTargetCapacityType"
    )
    total_target_capacity: Optional[float] = Field(None, alias="TotalTargetCapacity")
    on_demand_target_capacity: Optional[float] = Field(
        None, alias="OnDemandTargetCapacity"
    )
    spot_target_capacity: Optional[float] = Field(None, alias="SpotTargetCapacity")


class OnDemandOptions(BaseModel):
    allocation_strategy: Optional[str] = Field(None, alias="AllocationStrategy")
    max_target_capacity: Optional[float] = Field(None, alias="MaxTargetCapacity")
    max_instance_count: Optional[float] = Field(None, alias="MaxInstanceCount")
    instance_pool_constraint_filter_disabled: Optional[bool] = Field(
        None, alias="InstancePoolConstraintFilterDisabled"
    )


class SpotOptions(BaseModel):
    allocation_strategy: Optional[str] = Field(None, alias="AllocationStrategy")
    max_target_capacity: Optional[float] = Field(None, alias="MaxTargetCapacity")
    max_instance_count: Optional[float] = Field(None, alias="MaxInstanceCount")
    instance_pools_to_use_count: Optional[float] = Field(
        None, alias="InstancePoolsToUseCount"
    )
    instance_pool_constraint_filter_disabled: Optional[bool] = Field(
        None, alias="InstancePoolConstraintFilterDisabled"
    )


class ExistingInstances(BaseModel):
    operating_system: Optional[str] = Field(None, alias="OperatingSystem")
    availability_zone: Optional[str] = Field(None, alias="AvailabilityZone")
    tag: Optional[float] = None
    count: Optional[float] = Field(None, alias="Count")
    instance_type: Optional[str] = Field(None, alias="InstanceType")
    market_option: Optional[str] = Field(None, alias="MarketOption")


class LaunchTemplateSpecification(BaseModel):
    version: Optional[float] = Field(None, alias="Version")
    launch_template_id: Optional[str] = Field(None, alias="LaunchTemplateId")


class LaunchTemplateConfigs(BaseModel):
    launch_template_specification: Optional[LaunchTemplateSpecification] = Field(
        None, alias="LaunchTemplateSpecification"
    )
    overrides: Optional[list[dict]] = Field(None, alias="Overrides")
    tag: Optional[float] = None


class Tag(BaseModel):
    value: Optional[str] = Field(None, alias="Value")
    tag: Optional[float] = None
    key: Optional[str] = Field(None, alias="Key")


class TagSpecification(BaseModel):
    tag: Optional[Tag] = Field(None, alias="Tag")
    resource_type: Optional[str] = Field(None, alias="ResourceType")


class CreateFleetRequest(BaseModel):
    target_capacity_specification: Optional[TargetCapacitySpecification] = Field(
        None, alias="TargetCapacitySpecification"
    )
    on_demand_options: Optional[OnDemandOptions] = Field(None, alias="OnDemandOptions")
    spot_options: Optional[SpotOptions] = Field(None, alias="SpotOptions")
    existing_instances: Optional[ExistingInstances] = Field(
        None, alias="ExistingInstances"
    )
    launch_template_configs: Optional[LaunchTemplateConfigs] = Field(
        None, alias="LaunchTemplateConfigs"
    )
    tag_specification: Optional[TagSpecification] = Field(
        None, alias="TagSpecification"
    )
    type: Optional[str] = Field(None, alias="Type")
    client_token: Optional[str] = Field(None, alias="ClientToken")


class CreateFleetResponse(BaseModel):
    fleet_instance_set: Optional[dict] = Field(None, alias="fleetInstanceSet")
    xmlns: Optional[str] = None
    request_id: Optional[str] = Field(None, alias="requestId")
    fleet_id: Optional[str] = Field(None, alias="fleetId")
    error_set: Optional[dict] = Field(None, alias="errorSet")


# --- Network interface (response-level) ---


class NetworkInterface(BaseModel):
    group_set: Optional[GroupSet2] = Field(None, alias="groupSet")
    tag_set: Optional[dict] = Field(None, alias="tagSet")
    ipv6_addresses_set: Optional[dict] = Field(None, alias="ipv6AddressesSet")
    private_ip_addresses_set: Optional[PrivateIpAddressesSet1] = Field(
        None, alias="privateIpAddressesSet"
    )
    network_interface_id: Optional[str] = Field(None, alias="networkInterfaceId")
    subnet_id: Optional[str] = Field(None, alias="subnetId")
    requester_id: Optional[str] = Field(None, alias="requesterId")
    description: Optional[str] = None
    owner_id: Optional[str] = Field(None, alias="ownerId")
    source_dest_check: Optional[bool] = Field(None, alias="sourceDestCheck")
    availability_zone: Optional[str] = Field(None, alias="availabilityZone")
    requester_managed: Optional[bool] = Field(None, alias="requesterManaged")
    private_ip_address: Optional[str] = Field(None, alias="privateIpAddress")
    interface_type: Optional[str] = Field(None, alias="interfaceType")
    mac_address: Optional[str] = Field(None, alias="macAddress")
    vpc_id: Optional[str] = Field(None, alias="vpcId")
    status: Optional[str] = None


# --- Request / response parameter sets ---


class GroupSet1Item(BaseModel):
    group_id: Optional[str] = Field(None, alias="groupId")


class GroupSet1(BaseModel):
    items: Optional[list[GroupSet1Item]] = None


class InstancesSet1Item(BaseModel):
    instance_id: Optional[str] = Field(None, alias="instanceId")
    image_id: Optional[str] = Field(None, alias="imageId")
    min_count: Optional[float] = Field(None, alias="minCount")
    max_count: Optional[float] = Field(None, alias="maxCount")


class InstancesSet1(BaseModel):
    items: Optional[list[InstancesSet1Item]] = None


class NetworkInterfaceSetItem(BaseModel):
    subnet_id: Optional[str] = Field(None, alias="subnetId")
    device_index: Optional[float] = Field(None, alias="deviceIndex")


class NetworkInterfaceSet(BaseModel):
    items: Optional[list[NetworkInterfaceSetItem]] = None


class TagSpecificationSetItem(BaseModel):
    resource_type: Optional[str] = Field(None, alias="resourceType")
    tags: Optional[list[TagItem]] = None


class TagSpecificationSet(BaseModel):
    items: Optional[list[TagSpecificationSetItem]] = None


class Monitoring(BaseModel):
    enabled: Optional[bool] = None


class SpotOptions1(BaseModel):
    spot_instance_type: Optional[str] = Field(None, alias="spotInstanceType")
    max_price: Optional[str] = Field(None, alias="maxPrice")


class InstanceMarketOptions(BaseModel):
    spot_options: Optional[SpotOptions1] = Field(None, alias="spotOptions")
    market_type: Optional[str] = Field(None, alias="marketType")


class LaunchTemplate(BaseModel):
    launch_template_id: Optional[str] = Field(None, alias="launchTemplateId")
    version: Optional[str] = None


# --- Top-level request/response ---


class RequestParameters(BaseModel):
    create_launch_template_request: Optional[CreateLaunchTemplateRequest] = Field(
        None, alias="CreateLaunchTemplateRequest"
    )
    group_set: Optional[GroupSet1] = Field(None, alias="groupSet")
    instances_set: Optional[InstancesSet1] = Field(None, alias="instancesSet")
    create_fleet_request: Optional[CreateFleetRequest] = Field(
        None, alias="CreateFleetRequest"
    )
    delete_launch_template_request: Optional[DeleteLaunchTemplateRequest] = Field(
        None, alias="DeleteLaunchTemplateRequest"
    )
    private_ip_addresses_set: Optional[dict] = Field(
        None, alias="privateIpAddressesSet"
    )
    network_interface_set: Optional[NetworkInterfaceSet] = Field(
        None, alias="networkInterfaceSet"
    )
    block_device_mapping: Optional[dict] = Field(None, alias="blockDeviceMapping")
    tag_specification_set: Optional[TagSpecificationSet] = Field(
        None, alias="tagSpecificationSet"
    )
    monitoring: Optional[Monitoring] = None
    instance_market_options: Optional[InstanceMarketOptions] = Field(
        None, alias="instanceMarketOptions"
    )
    launch_template: Optional[LaunchTemplate] = Field(None, alias="launchTemplate")
    subnet_id: Optional[str] = Field(None, alias="subnetId")
    user_data: Optional[str] = Field(None, alias="userData")
    group_id: Optional[str] = Field(None, alias="groupId")
    description: Optional[str] = None
    availability_zone: Optional[str] = Field(None, alias="availabilityZone")
    vpc_id: Optional[str] = Field(None, alias="vpcId")
    network_interface_id: Optional[str] = Field(None, alias="networkInterfaceId")
    client_token: Optional[str] = Field(None, alias="clientToken")
    instance_type: Optional[str] = Field(None, alias="instanceType")
    ipv6_address_count: Optional[float] = Field(None, alias="ipv6AddressCount")
    group_name: Optional[str] = Field(None, alias="groupName")
    disable_api_termination: Optional[bool] = Field(None, alias="disableApiTermination")
    group_description: Optional[str] = Field(None, alias="groupDescription")


class ResponseElements(BaseModel):
    instances_set: Optional[InstancesSet] = Field(None, alias="instancesSet")
    create_fleet_response: Optional[CreateFleetResponse] = Field(
        None, alias="CreateFleetResponse"
    )
    delete_launch_template_response: Optional[DeleteLaunchTemplateResponse] = Field(
        None, alias="DeleteLaunchTemplateResponse"
    )
    network_interface: Optional[NetworkInterface] = Field(
        None, alias="networkInterface"
    )
    create_launch_template_response: Optional[DeleteLaunchTemplateResponse] = Field(
        None, alias="CreateLaunchTemplateResponse"
    )
    group_set: Optional[dict] = Field(None, alias="groupSet")
    return_: Optional[bool] = Field(None, alias="_return")
    requester_id: Optional[str] = Field(None, alias="requesterId")
    reservation_id: Optional[str] = Field(None, alias="reservationId")
    request_id: Optional[str] = Field(None, alias="requestId")
    group_id: Optional[str] = Field(None, alias="groupId")
    owner_id: Optional[str] = Field(None, alias="ownerId")


class AWSAPICallViaCloudTrail(BaseModel):
    """CloudTrail detail payload for aws.ec2 API calls."""

    response_elements: Optional[ResponseElements] = Field(
        None, alias="responseElements"
    )
    request_parameters: Optional[RequestParameters] = Field(
        None, alias="requestParameters"
    )
    user_identity: UserIdentity = Field(..., alias="userIdentity")
    event_id: str = Field(..., alias="eventID")
    aws_region: str = Field(..., alias="awsRegion")
    event_version: str = Field(..., alias="eventVersion")
    source_ip_address: str = Field(..., alias="sourceIPAddress")
    event_source: str = Field(..., alias="eventSource")
    error_message: Optional[str] = Field(None, alias="errorMessage")
    error_code: Optional[str] = Field(None, alias="errorCode")
    user_agent: str = Field(..., alias="userAgent")
    event_type: str = Field(..., alias="eventType")
    request_id: str = Field(..., alias="requestID")
    event_time: datetime = Field(..., alias="eventTime")
    event_name: str = Field(..., alias="eventName")


class AWSEvent(BaseModel):
    """Top-level EventBridge envelope for 'AWS API Call via CloudTrail' (aws.ec2)."""

    model_config = {"populate_by_name": True}

    detail: AWSAPICallViaCloudTrail
    detail_type: str = Field(..., alias="detail-type")
    resources: list[str]
    id: str
    source: str
    time: datetime
    region: str
    version: str
    account: str
