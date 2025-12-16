import httpx
import asyncio
from typing import Optional
from models import (
    FindHouseholdValveParams,
    UpdateHouseholdValveParams,
    DeviceInfo,
    UpdateControlParams,
    FindNetEquipmentParams,
    FindHouseholdMeterCurrentDataParams
)

class HouseValveClient:
    def __init__(self, base_url, token):
        self.base_url = base_url
        self.token = token
        self.headers = {
            'Authorization': f'Bearer {self.token}',
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        # 创建httpx异步客户端
        self.client = httpx.AsyncClient(headers=self.headers)
    
    async def __aenter__(self):
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        # 关闭httpx客户端
        await self.client.aclose()
    
    async def find_household_valve(self, params: Optional[FindHouseholdValveParams] = None):
        """
        根据户阀编号查询户阀信息
        
        :param params: 查询参数模型，默认为None
        :return: 户阀信息列表
        """
        url = f'{self.base_url}/v4.0/maintain/houseValve/findHouseholdValve'
        
        # 如果没有提供参数，使用默认参数
        if params is None:
            params = FindHouseholdValveParams()
        
        # 将Pydantic模型转换为字典，并转换键名（下划线转驼峰）
        api_params = {
            'pageIndex': params.page_index,
            'pageSize': params.page_size,
            'sortName': params.sort_name,
            'sortType': params.sort_type,
            'treeId': params.tree_id,
            'treeLevel': params.tree_level,
            'parentLevelId': params.parent_level_id,
            'factoryId': params.factory_id,
            'modelId': params.model_id,
            'netEquName': params.net_equ_name,
            'serialNo': params.serial_no,
            'port': params.port,
            'baudRate': params.baud_rate,
            'checkBit': params.check_bit,
            'index': params.index,
            'communicationType': params.communication_type,
            'roomType': params.room_type,
            'installSite': params.install_site,
            'equipmentUse': params.equipment_use
        }
        
        try:
            response = await self.client.get(url, params=api_params)
            response.raise_for_status()  # 抛出HTTP错误
            return response.json()
        except httpx.RequestError as e:
            print(f"请求失败: {e}")
            return None
    
    async def update_household_valve(self, params: UpdateHouseholdValveParams):
        """
        更新户阀信息
        
        :param params: 更新参数模型
        :return: 更新结果
        """
        url = f'{self.base_url}/v4.0/maintain/houseValve/updateHouseholdValve'
        
        # 构建请求体
        data = {
            'stationBranchName': params.station_branch_name,
            'stationBranchId': params.station_branch_id,
            'serialNo': params.serial_no,
            'type': params.type_valve,
            'unitId': params.unit_id,
            'factoryId': params.factory_id,
            'modelId': params.model_id,
            'netEquId': params.net_equ_id,
            'collectorId': params.collector_id,
            'port': params.port,
            'baudRate': params.baud_rate,
            'checkBit': params.check_bit,
            'index': params.index,
            'caliber': params.caliber,
            'isReadCard': params.is_read_card,
            'isTemControl': params.is_tem_control,
            'isSettingTem': params.is_setting_tem,
            'isTemRange': params.is_tem_range,
            'isLockTem': params.is_lock_tem,
            'detailPosition': params.detail_position,
            'intermediatePath': params.intermediate_path,
            'enabled': params.enabled,
            'installDate': params.install_date,
            'createDate': params.create_date,
            'memo': params.memo,
            'uniqueId': params.unique_id,
            'panelSerialNo': params.panel_serial_no,
            'communicationType': params.communication_type,
            'panelId': params.panel_id,
            'roomPanelId': params.room_panel_id,
            'identificationCode': params.identification_code,
            'equipmentUse': params.equipment_use,
            'installSite': params.install_site
        }
        
        try:
            response = await self.client.put(url, json=data)
            response.raise_for_status()  # 抛出HTTP错误
            return response.json()
        except httpx.RequestError as e:
            print(f"请求失败: {e}")
            return None
    
    async def update_control(self, params: UpdateControlParams):
        """
        采集器下发档案
        
        :param params: 下发档案参数模型
        :return: 更新结果
        """
        url = f'{self.base_url}/v4.0/maintain/buildAiControl/updateControl'
        
        # 将Pydantic模型转换为API所需的格式
        device_list = []
        for device in params.devices:
            device_list.append({
                'serialNo': device.serial_no,
                'guid': device.guid
            })
        
        try:
            response = await self.client.post(url, json=device_list)
            response.raise_for_status()
            return response.json()
        except httpx.RequestError as e:
            print(f"请求失败: {e}")
            return None
    
    async def update_control_by_serial_no(self, serial_no_list):
        """
        根据采集器编号列表下发档案（自动查询guid）
        
        :param serial_no_list: 采集器编号列表，格式为 ['serial_no1', 'serial_no2', ...]
        :return: 更新结果，包含成功状态、消息和更新结果
        """
        result = {
            'success': False,
            'message': '',
            'update_result': None,
            'device_info': []
        }
        
        if not serial_no_list:
            result['message'] = "采集器编号列表不能为空"
            return result
        
        try:
            # 1. 遍历采集器编号，查询每个采集器的guid
            device_list = []
            missing_devices = []
            
            for serial_no in serial_no_list:
                # 根据serialNo查询采集器信息
                # 使用Pydantic模型调用find_net_equipment
                find_params = FindNetEquipmentParams(
                    serial_no=serial_no,
                    page_size=1
                )
                net_equ_result = await self.find_net_equipment(find_params)
                
                if net_equ_result and net_equ_result.get('resultCode') == 0:
                    data = net_equ_result.get('data', {})
                    equ_list = data.get('data', [])
                    
                    if equ_list:
                        # 获取第一个匹配的采集器信息
                        equ_info = equ_list[0]
                        guid = equ_info.get('guid')
                        
                        if guid:
                            device_list.append({
                                'serialNo': serial_no,
                                'guid': guid
                            })
                            result['device_info'].append({
                                'serial_no': serial_no,
                                'guid': guid,
                                'found': True
                            })
                        else:
                            missing_devices.append(serial_no)
                            result['device_info'].append({
                                'serial_no': serial_no,
                                'guid': None,
                                'found': False,
                                'reason': '未找到guid'
                            })
                    else:
                        missing_devices.append(serial_no)
                        result['device_info'].append({
                            'serial_no': serial_no,
                            'guid': None,
                            'found': False,
                            'reason': '未找到采集器信息'
                        })
                else:
                    missing_devices.append(serial_no)
                    result['device_info'].append({
                        'serial_no': serial_no,
                        'guid': None,
                        'found': False,
                        'reason': '查询失败'
                    })
            
            if missing_devices:
                result['message'] = f"部分采集器查询失败：{missing_devices}"
            
            # 2. 如果有找到的设备，进行下发档案
            if device_list:
                # 使用Pydantic模型调用update_control
                # 先将device_list转换为DeviceInfo对象列表
                device_info_list = []
                for device in device_list:
                    device_info_list.append(DeviceInfo(serial_no=device['serialNo'], guid=device['guid']))
                
                # 创建UpdateControlParams对象
                control_params = UpdateControlParams(devices=device_info_list)
                
                update_result = await self.update_control(control_params)
                result['update_result'] = update_result
                
                if update_result and update_result.get('resultCode') == 0:
                    result['success'] = True
                    if missing_devices:
                        result['message'] = f"部分设备下发成功，部分设备查询失败：{missing_devices}"
                    else:
                        result['message'] = "所有设备下发成功"
            else:
                result['message'] = "没有找到有效的设备信息，无法下发档案"
                
        except Exception as e:
            result['message'] = f"处理失败：{str(e)}"
            
        return result
    
    async def find_net_equipment(self, params: Optional[FindNetEquipmentParams] = None):
        """
        根据采集器编号查询采集器信息
        
        :param params: 查询参数模型，默认为None
        :return: 采集器信息列表
        """
        url = f'{self.base_url}/v4.0/maintain/netEquManage/findNetEqu'
        
        # 如果没有提供参数，使用默认参数
        if params is None:
            params = FindNetEquipmentParams()
        
        # 将Pydantic模型转换为字典，并转换键名（下划线转驼峰）
        api_params = {
            'equipmentTypeId': params.equipment_type_id,
            'factoryId': params.factory_id,
            'modelId': params.model_id,
            'meterNo': params.meter_no,
            'serialNo': params.serial_no,
            'installType': params.install_type,
            'treeId': params.tree_id,
            'treeLevel': params.tree_level,
            'parentLevelId': params.parent_level_id,
            'pageIndex': params.page_index,
            'pageSize': params.page_size,
            'sortName': params.sort_name,
            'sortType': params.sort_type
        }
        
        try:
            response = await self.client.get(url, params=api_params)
            response.raise_for_status()
            return response.json()
        except httpx.RequestError as e:
            print(f"请求失败: {e}")
            return None
    
    async def find_household_meter_current_data(self, params: FindHouseholdMeterCurrentDataParams):
        """
        根据阀号查询户阀抄通状态
        
        :param params: 查询参数模型
        :return: 户阀抄通状态信息
        """
        url = f'{self.base_url}/v4.0/meter/heatMonitor/findHouseholdMeterCurrentDataAdvanced'
        
        # 构建advanceCondition和advanceName参数
        # 注意：不要手动URL编码，让httpx自动处理
        advance_condition = f"((oc_v.serialNo='{params.serial_no}'))"
        advance_name = f"(户阀编号='{params.serial_no}')"
        
        # 构建完整的API参数
        api_params = {
            'advanceCondition': advance_condition,
            'advanceName': advance_name,
            'uniqueIds': params.unique_ids,
            'save': params.save,
            'saveName': params.save_name,
            'menuId': params.menu_id,
            'treeId': params.tree_id,
            'treeLevel': params.tree_level,
            'parentLevelId': params.parent_level_id,
            'flag': params.flag,
            'buildAndFloors': params.build_and_floors,
            'sortName': params.sort_name,
            'sortType': params.sort_type,
            'pageSize': params.page_size,
            'pageIndex': params.page_index
        }
        
        try:
            response = await self.client.get(url, params=api_params)
            response.raise_for_status()
            return response.json()
        except httpx.RequestError as e:
            print(f"请求失败: {e}")
            return None
    
    async def update_valve_serial_no(self, query_serial_no, query_address, new_serial_no):
        """
        根据查询的阀号和地址，更新阀号为新的阀号
        
        :param query_serial_no: 查询用的阀号
        :param query_address: 查询用的地址
        :param new_serial_no: 更新后的新阀号
        :return: 更新结果字典，包含成功状态、更新结果和验证结果
        """
        result = {
            'success': False,
            'message': '',
            'update_result': None,
            'verify_result': None
        }
        
        try:
            # 1. 根据serialNo查询户阀信息列表
            search_params = FindHouseholdValveParams(
                serial_no=query_serial_no,
                page_size=20,
                tree_id='',
                tree_level=0
            )
            search_result = await self.find_household_valve(search_params)
            
            if not search_result:
                result['message'] = "查询失败：API调用失败"
                return result
            
            if search_result.get('resultCode') != 0:
                result['message'] = f"查询失败：API返回错误 - {search_result.get('message', '未知错误')}"
                return result
            
            if not search_result.get('data', {}).get('data'):
                result['message'] = f"查询失败：未找到serialNo为'{query_serial_no}'的户阀信息"
                return result
            
            # 2. 从查询结果中通过address找到唯一匹配的数据
            valve_list = search_result['data']['data']
            matched_valve = None
            
            for valve in valve_list:
                if valve.get('address') == query_address:
                    matched_valve = valve
                    break
            
            if not matched_valve:
                result['message'] = f"未找到address为'{query_address}'的户阀信息"
                return result
            
            # 3. 构建基础更新数据
            base_update_data = {
                "station_branch_name": matched_valve.get('stationBranchName', ''),
                "station_branch_id": matched_valve.get('stationBranchId'),
                "serial_no": matched_valve.get('serialNo'),
                "type_valve": matched_valve.get('type'),
                "unit_id": matched_valve.get('unitName'),
                "factory_id": matched_valve.get('factoryId'),
                "model_id": matched_valve.get('modelId'),
                "net_equ_id": matched_valve.get('netEquId'),
                "collector_id": matched_valve.get('collectorId'),
                "port": matched_valve.get('port'),
                "baud_rate": matched_valve.get('baudRate'),
                "check_bit": matched_valve.get('checkBit'),
                "index": matched_valve.get('index'),
                "caliber": matched_valve.get('caliber'),
                "is_read_card": matched_valve.get('isReadCard') == '支持',
                "is_tem_control": matched_valve.get('isTemControl') == '支持',
                "is_setting_tem": matched_valve.get('isSettingTem') == '支持',
                "is_tem_range": matched_valve.get('isTemRange') == '支持',
                "is_lock_tem": matched_valve.get('isLockTem') == '支持',
                "detail_position": matched_valve.get('detailPosition'),
                "intermediate_path": matched_valve.get('intermediatePath'),
                "enabled": matched_valve.get('enabled', True),
                "install_date": matched_valve.get('installDate'),
                "create_date": matched_valve.get('createDate'),
                "memo": matched_valve.get('memo'),
                "unique_id": matched_valve.get('uniqueId'),
                "panel_serial_no": matched_valve.get('panelSerialNo'),
                "communication_type": matched_valve.get('communicationType', 1),
                "panel_id": matched_valve.get('panelId'),
                "room_panel_id": matched_valve.get('roomPanelId'),
                "identification_code": matched_valve.get('identificationCode'),
                "equipment_use": matched_valve.get('equipmentUse', '调节阀'),
                "install_site": matched_valve.get('installSite')
            }
            
            # 4. 设置更新的新阀号
            update_changes = {
                "serial_no": new_serial_no
            }
            
            # 5. 组合最终的更新数据
            final_update_data = {**base_update_data, **update_changes}
            
            # 6. 执行更新操作
            # 使用Pydantic模型调用update_household_valve
            update_params = UpdateHouseholdValveParams(**final_update_data)
            update_result = await self.update_household_valve(update_params)
            result['update_result'] = update_result
            
            if not update_result:
                result['message'] = "更新失败：API调用失败"
                return result
            
            if update_result.get('resultCode') != 0:
                result['message'] = f"更新失败：API返回错误 - {update_result.get('message', '未知错误')}"
                return result
            
            # 7. 验证更新结果 - 使用更新后的serialNo查询
            updated_serial_no = final_update_data['serial_no']
            # 使用Pydantic模型调用find_household_valve
            verify_params = FindHouseholdValveParams(serial_no=updated_serial_no)
            verify_result = await self.find_household_valve(verify_params)
            result['verify_result'] = verify_result
            
            if verify_result and verify_result.get('resultCode') == 0 and verify_result.get('data', {}).get('data'):
                # 查找匹配的验证结果
                matched_verify_valve = None
                for valve in verify_result['data']['data']:
                    if valve.get('address') == query_address:
                        matched_verify_valve = valve
                        break
                
                if matched_verify_valve and matched_verify_valve.get('serialNo') == new_serial_no:
                    result['success'] = True
                    result['message'] = f"成功将阀号从'{query_serial_no}'更新为'{new_serial_no}'"
                else:
                    result['message'] = f"验证失败：未找到更新后的阀号或serialNo不匹配"
            else:
                result['message'] = f"验证失败：使用更新后的serialNo '{updated_serial_no}' 查询不到数据"
                
        except Exception as e:
            result['message'] = f"处理失败：{str(e)}"
            
        return result

# 示例用法
async def main():
    # 使用异步上下文管理器初始化客户端
    async with HouseValveClient(
        base_url="http://112.53.73.250:2288",
        token="a704c946-b32e-49eb-85d8-f0a576695d78"
    ) as client:
        # 示例1：使用封装的方法更新阀号
        # print("=== 示例1：更新阀号 ===")
        # update_result = await client.update_valve_serial_no(
        #     query_serial_no="25249851",
        #     query_address="广安苑小区-1#-一单元-2302",
        #     new_serial_no="25249815"
        # )
        
        # print(f"更新结果: {update_result['message']}")
        # print(f"成功状态: {update_result['success']}")
        
        # if update_result['update_result']:
        #     print(f"API更新结果: {update_result['update_result']}")
        
        # if update_result['verify_result']:
        #     print(f"验证查询结果: {'成功' if update_result['success'] else '失败'}")
        
        # 示例2：采集器下发档案（使用Pydantic模型）
        # print("\n=== 示例2：采集器下发档案（使用Pydantic模型） ===")
        # # 创建设备信息列表
        # devices = [
        #     DeviceInfo(serial_no="25001318", guid="NEQ5217"),
        #     DeviceInfo(serial_no="25001461", guid="NEQ5221")
        # ]
        # # 创建更新参数
        # control_params = UpdateControlParams(devices=devices)
        # control_result = await client.update_control(control_params)
        # print(f"采集器下发档案结果: {control_result}")
        
        # # 示例2.1：优化后的采集器下发档案（自动查询guid）
        # print("\n=== 示例2.1：优化后的采集器下发档案（自动查询guid） ===")
        # serial_no_list = ["25001318", "25001461"]
        # optimized_result = await client.update_control_by_serial_no(serial_no_list)
        # print(f"优化后的下发结果: {optimized_result}")
        # print(f"成功状态: {optimized_result['success']}")
        # print(f"消息: {optimized_result['message']}")
        
        # if optimized_result['update_result']:
        #     print(f"API返回: {optimized_result['update_result']}")
        
        # # 打印设备详情
        # print("设备详情:")
        # for device in optimized_result['device_info']:
        #     status = "成功" if device['found'] else "失败"
        #     print(f"  - serial_no: {device['serial_no']}, guid: {device['guid']}, 状态: {status}")
        
        # 示例3：根据采集器编号查询采集器信息（使用Pydantic模型）
        print("\n=== 示例3：根据采集器编号查询采集器信息（使用Pydantic模型） ===")
        # 根据serialNo查询
        serial_no = "25001267"
        find_params = FindNetEquipmentParams(serial_no=serial_no)
        net_equ_result = await client.find_net_equipment(find_params)
        print(f"根据serialNo '{serial_no}' 查询结果: {net_equ_result}")
        
        # 根据factoryId查询
        factory_id = "437"
        find_params2 = FindNetEquipmentParams(factory_id=factory_id, page_size=10)
        net_equ_result2 = await client.find_net_equipment(find_params2)
        if net_equ_result2 and net_equ_result2.get('resultCode') == 0:
            total = net_equ_result2.get('data', {}).get('total', 0)
            print(f"根据factoryId '{factory_id}' 查询结果: 共找到 {total} 条记录")
        
        # 示例4：根据阀号查询户阀抄通状态（使用Pydantic模型）
        print("\n=== 示例4：根据阀号查询户阀抄通状态 ===")
        valve_serial_no = "24818174"
        meter_params = FindHouseholdMeterCurrentDataParams(serial_no=valve_serial_no)
        meter_result = await client.find_household_meter_current_data(meter_params)
        print(f"根据阀号 '{valve_serial_no}' 查询抄通状态结果: {meter_result}")
        
        if meter_result and meter_result.get('resultCode') == 0:
            data = meter_result.get('data', {})
            total = data.get('total', 0)
            print(f"查询到 {total} 条记录")
            if total > 0:
                records = data.get('data', [])
                for record in records:
                    print(f"  - 设备编号: {record.get('serialNo')}, 抄通状态: {record.get('commStatus')}")
        
        # 示例5：使用自定义参数测试户阀抄通状态查询
        print("\n=== 示例5：使用自定义参数测试户阀抄通状态查询 ===")
        # 使用样本URL中类似的参数
        custom_meter_params = FindHouseholdMeterCurrentDataParams(
            serial_no="25044582",
            tree_id="001014",
            tree_level=2,
            parent_level_id="1-001"
        )
        custom_meter_result = await client.find_household_meter_current_data(custom_meter_params)
        print(f"使用自定义参数查询结果: {custom_meter_result}")

if __name__ == "__main__":
    # 运行异步主函数
    asyncio.run(main())
