import requests

class HouseValveClient:
    def __init__(self, base_url, token):
        self.base_url = base_url
        self.token = token
        self.headers = {
            'Authorization': f'Bearer {self.token}',
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
    
    def find_household_valve(self, page_index=1, page_size=5000, sort_name='', sort_type='', 
                            tree_id='001', tree_level=1, parent_level_id='', factory_id='', 
                            model_id='', net_equ_name='', serial_no='', port='', baud_rate='', 
                            check_bit='', index='', communication_type='', room_type='', 
                            install_site='', equipment_use=''):
        url = f'{self.base_url}/v4.0/maintain/houseValve/findHouseholdValve'
        params = {
            'pageIndex': page_index,
            'pageSize': page_size,
            'sortName': sort_name,
            'sortType': sort_type,
            'treeId': tree_id,
            'treeLevel': tree_level,
            'parentLevelId': parent_level_id,
            'factoryId': factory_id,
            'modelId': model_id,
            'netEquName': net_equ_name,
            'serialNo': serial_no,
            'port': port,
            'baudRate': baud_rate,
            'checkBit': check_bit,
            'index': index,
            'communicationType': communication_type,
            'roomType': room_type,
            'installSite': install_site,
            'equipmentUse': equipment_use
        }
        
        try:
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"请求失败: {e}")
            return None
    
    def update_household_valve(self, station_branch_name, station_branch_id, serial_no, type_valve, 
                             unit_id, factory_id, model_id, net_equ_id, collector_id=None, 
                             port=None, baud_rate=None, check_bit=None, index=None, caliber=None, 
                             is_read_card=False, is_tem_control=False, is_setting_tem=False, 
                             is_tem_range=False, is_lock_tem=False, detail_position=None, 
                             intermediate_path=None, enabled=True, install_date=None, 
                             create_date=None, memo=None, unique_id=None, panel_serial_no=None, 
                             communication_type=1, panel_id=None, room_panel_id=None, 
                             identification_code=None, equipment_use='调节阀', install_site=None):
        url = f'{self.base_url}/v4.0/maintain/houseValve/updateHouseholdValve'
        
        data = {
            'stationBranchName': station_branch_name,
            'stationBranchId': station_branch_id,
            'serialNo': serial_no,
            'type': type_valve,
            'unitId': unit_id,
            'factoryId': factory_id,
            'modelId': model_id,
            'netEquId': net_equ_id,
            'collectorId': collector_id,
            'port': port,
            'baudRate': baud_rate,
            'checkBit': check_bit,
            'index': index,
            'caliber': caliber,
            'isReadCard': is_read_card,
            'isTemControl': is_tem_control,
            'isSettingTem': is_setting_tem,
            'isTemRange': is_tem_range,
            'isLockTem': is_lock_tem,
            'detailPosition': detail_position,
            'intermediatePath': intermediate_path,
            'enabled': enabled,
            'installDate': install_date,
            'createDate': create_date,
            'memo': memo,
            'uniqueId': unique_id,
            'panelSerialNo': panel_serial_no,
            'communicationType': communication_type,
            'panelId': panel_id,
            'roomPanelId': room_panel_id,
            'identificationCode': identification_code,
            'equipmentUse': equipment_use,
            'installSite': install_site
        }
        
        try:
            response = requests.put(url, headers=self.headers, json=data)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"请求失败: {e}")
            return None

# 恢复数据脚本
if __name__ == "__main__":
    # 初始化客户端
    client = HouseValveClient(
        base_url="http://112.53.73.250:2288",
        token="1a6cd7dc-fb1c-4aca-8de7-ab0142d81505"
    )
    
    # 恢复参数：将serialNo从25254089改回24820311
    print("=== 开始恢复户阀数据 ===")
    
    # 1. 根据修改后的serialNo查询户阀信息
    modified_serial_no = "25254089"
    result = client.find_household_valve(serial_no=modified_serial_no)
    
    if not (result and result.get('resultCode') == 0 and result.get('data', {}).get('data')):
        print("查询失败，无法获取户阀信息")
        exit()
    
    # 2. 获取需要恢复的数据
    valve_info = result['data']['data'][0]
    print(f"找到需要恢复的数据：serialNo={valve_info.get('serialNo')}, address={valve_info.get('address')}")
    
    # 3. 构建恢复数据，将serialNo改回原始值
    recovery_data = {
        "station_branch_name": valve_info.get('stationBranchName', ''),
        "station_branch_id": valve_info.get('stationBranchId'),
        "serial_no": "24820311",  # 恢复为原始serialNo
        "type_valve": valve_info.get('type'),
        "unit_id": valve_info.get('unitName'),
        "factory_id": valve_info.get('factoryId'),
        "model_id": valve_info.get('modelId'),
        "net_equ_id": valve_info.get('netEquId'),
        "collector_id": valve_info.get('collectorId'),
        "port": valve_info.get('port'),
        "baud_rate": valve_info.get('baudRate'),
        "check_bit": valve_info.get('checkBit'),
        "index": valve_info.get('index'),
        "caliber": valve_info.get('caliber'),
        "is_read_card": valve_info.get('isReadCard') == '支持',
        "is_tem_control": valve_info.get('isTemControl') == '支持',
        "is_setting_tem": valve_info.get('isSettingTem') == '支持',
        "is_tem_range": valve_info.get('isTemRange') == '支持',
        "is_lock_tem": valve_info.get('isLockTem') == '支持',
        "detail_position": valve_info.get('detailPosition'),
        "intermediate_path": valve_info.get('intermediatePath'),
        "enabled": valve_info.get('enabled', True),
        "install_date": valve_info.get('installDate'),
        "create_date": valve_info.get('createDate'),
        "memo": valve_info.get('memo'),
        "unique_id": valve_info.get('uniqueId'),
        "panel_serial_no": valve_info.get('panelSerialNo'),
        "communication_type": valve_info.get('communicationType', 1),
        "panel_id": valve_info.get('panelId'),
        "room_panel_id": valve_info.get('roomPanelId'),
        "identification_code": valve_info.get('identificationCode'),
        "equipment_use": valve_info.get('equipmentUse', '调节阀'),
        "install_site": valve_info.get('installSite')
    }
    
    # 4. 执行恢复操作
    print(f"恢复操作：将serialNo从'{modified_serial_no}'改回'24820311'")
    recovery_result = client.update_household_valve(**recovery_data)
    
    if recovery_result:
        print("恢复成功:")
        print(recovery_result)
        
        # 5. 验证恢复结果
        print("\n=== 验证恢复结果 ===")
        verify_result = client.find_household_valve(serial_no="24820311")
        if verify_result and verify_result.get('resultCode') == 0 and verify_result.get('data', {}).get('data'):
            print(f"恢复后的serialNo '24820311' 验证成功：")
            for valve in verify_result['data']['data']:
                if valve.get('address') == valve_info.get('address'):
                    print("恢复后的户阀信息：")
                    print(valve)
                    break
    else:
        print("恢复失败")
    
    print("\n=== 数据恢复完成 ===")
