from pydantic import BaseModel, Field
from typing import Optional


class FindHouseholdValveParams(BaseModel):
    """根据户阀编号查询户阀信息参数"""
    page_index: int = Field(default=1, description="页码")
    page_size: int = Field(default=5000, description="每页大小")
    sort_name: str = Field(default="", description="排序字段")
    sort_type: str = Field(default="", description="排序类型")
    tree_id: str = Field(default="001", description="树ID")
    tree_level: int = Field(default=1, description="树级别")
    parent_level_id: str = Field(default="", description="父级ID")
    factory_id: str = Field(default="", description="厂家ID")
    model_id: str = Field(default="", description="型号ID")
    net_equ_name: str = Field(default="", description="网络设备名称")
    serial_no: str = Field(default="", description="户阀编号")
    port: Optional[str] = Field(default=None, description="端口")
    baud_rate: Optional[str] = Field(default=None, description="波特率")
    check_bit: Optional[str] = Field(default=None, description="校验位")
    index: Optional[str] = Field(default=None, description="索引")
    communication_type: str = Field(default="", description="通信类型")
    room_type: str = Field(default="", description="房间类型")
    install_site: str = Field(default="", description="安装位置")
    equipment_use: str = Field(default="", description="设备用途")


class UpdateHouseholdValveParams(BaseModel):
    """更新户阀信息参数"""
    station_branch_name: str = Field(..., description="站点分支名称")
    station_branch_id: int = Field(..., description="站点分支ID")
    serial_no: str = Field(..., description="户阀编号")
    type_valve: str = Field(..., description="阀门类型")
    unit_id: str = Field(..., description="单元ID")
    factory_id: int = Field(..., description="厂家ID")
    model_id: int = Field(..., description="型号ID")
    net_equ_id: Optional[int] = Field(default=None, description="网络设备ID")
    collector_id: Optional[int] = Field(default=None, description="采集器ID")
    port: Optional[int] = Field(default=None, description="端口")
    baud_rate: Optional[str] = Field(default=None, description="波特率")
    check_bit: Optional[str] = Field(default=None, description="校验位")
    index: Optional[int] = Field(default=None, description="索引")
    caliber: Optional[int] = Field(default=None, description="口径")
    is_read_card: bool = Field(default=False, description="是否支持读卡")
    is_tem_control: bool = Field(default=False, description="是否支持温度控制")
    is_setting_tem: bool = Field(default=False, description="是否支持设置温度")
    is_tem_range: bool = Field(default=False, description="是否支持温度范围")
    is_lock_tem: bool = Field(default=False, description="是否支持锁定温度")
    detail_position: Optional[str] = Field(default=None, description="详细位置")
    intermediate_path: Optional[str] = Field(default=None, description="中间路径")
    enabled: bool = Field(default=True, description="是否启用")
    install_date: Optional[str] = Field(default=None, description="安装日期")
    create_date: Optional[str] = Field(default=None, description="创建日期")
    memo: Optional[str] = Field(default=None, description="备注")
    unique_id: Optional[int] = Field(default=None, description="唯一ID")
    panel_serial_no: Optional[str] = Field(default=None, description="面板序列号")
    communication_type: int = Field(default=1, description="通信类型")
    panel_id: Optional[int] = Field(default=None, description="面板ID")
    room_panel_id: Optional[int] = Field(default=None, description="房间面板ID")
    identification_code: Optional[str] = Field(default=None, description="识别码")
    equipment_use: str = Field(default="调节阀", description="设备用途")
    install_site: Optional[str] = Field(default=None, description="安装位置")


class DeviceInfo(BaseModel):
    """设备信息"""
    serial_no: str = Field(..., description="设备编号")
    guid: str = Field(..., description="设备GUID")


class UpdateControlParams(BaseModel):
    """采集器下发档案参数"""
    devices: list[DeviceInfo] = Field(..., description="设备列表")


class FindNetEquipmentParams(BaseModel):
    """查询网络设备参数"""
    equipment_type_id: str = Field(default="", description="设备类型ID")
    factory_id: str = Field(default="", description="厂家ID")
    model_id: str = Field(default="", description="型号ID")
    meter_no: str = Field(default="", description="仪表编号")
    serial_no: str = Field(default="", description="采集器编号")
    install_type: str = Field(default="", description="安装类型")
    tree_id: str = Field(default="001", description="树ID")
    tree_level: int = Field(default=1, description="树级别")
    parent_level_id: str = Field(default="", description="父级ID")
    page_index: int = Field(default=1, description="页码")
    page_size: int = Field(default=2000, description="每页大小")
    sort_name: str = Field(default="", description="排序字段")
    sort_type: str = Field(default="", description="排序类型")


class FindHouseholdMeterCurrentDataParams(BaseModel):
    """查询户阀抄通状态参数"""
    serial_no: str = Field(..., description="户阀编号")
    menu_id: str = Field(default="140207", description="菜单ID")
    tree_id: str = Field(default="001", description="树ID")
    tree_level: int = Field(default=1, description="树级别")
    parent_level_id: str = Field(default="", description="父级ID")
    flag: int = Field(default=1, description="标志位")
    page_index: int = Field(default=1, description="页码")
    page_size: int = Field(default=200, description="每页大小")
    sort_name: str = Field(default="", description="排序字段")
    sort_type: str = Field(default="", description="排序类型")
    unique_ids: str = Field(default="", description="唯一ID列表")
    save: bool = Field(default=False, description="是否保存查询")
    save_name: str = Field(default="", description="保存名称")
    build_and_floors: str = Field(default="", description="楼栋和楼层")
