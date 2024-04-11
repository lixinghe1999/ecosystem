//package sysu.sdcs.sensordatacollector;
//import com.wit.example.ble5.Bwt901ble;
//import com.wit.example.ble5.data.WitSensorKey;
//import com.wit.example.ble5.interfaces.IBwt901bleRecordObserver;
//import com.wit.witsdk.sensor.dkey.ShortKey;
//import com.wit.witsdk.sensor.dkey.StringKey;
//import com.wit.witsdk.sensor.modular.connector.modular.bluetooth.BluetoothBLE;
//import com.wit.witsdk.sensor.modular.connector.modular.bluetooth.BluetoothSPP;
//import com.wit.witsdk.sensor.modular.connector.modular.bluetooth.WitBluetoothManager;
//import com.wit.witsdk.sensor.modular.connector.modular.bluetooth.exceptions.BluetoothBLEException;
//import com.wit.witsdk.sensor.modular.connector.modular.bluetooth.interfaces.IBluetoothFoundObserver;
//import com.wit.witsdk.sensor.modular.device.exceptions.OpenDeviceException;
//
//import java.util.ArrayList;
//import java.util.Arrays;
//import java.util.List;
//import java.util.Objects;
//
//public class bluetooth {
//    private List<Bwt901ble> bwt901bleList = new ArrayList<>();
//
//    public void startDiscovery() {
//        // 开始搜索设备
//        // Turn off all device
//        for (int i = 0; i < bwt901bleList.size(); i++) {
//            Bwt901ble bwt901ble = bwt901bleList.get(i);
//            bwt901ble.removeRecordobserver(this);
//            bwt901ble.close();
//        }
//        // 清除所有设备
//        // Erase all devices
//        bwt901bleList.clear();
//        // 开始搜索蓝牙
//        // start searching for bluetooth
//        try {
//            // 获得蓝牙管理器
//            // get bluetooth manager
//            WitBluetoothManager bluetoothManager = witBluetoothManager.getInstance();
//            // 注册监听蓝牙
//            // Monitor communication signals
//            bluetoothManager.registerobserver(this);
//            // 指定要搜索的蓝牙名称
//            //Specify the Bluetooth name to search for
//            WitBluetoothManager.DeviceNameFilter = Arrays.asList("WT"),
//                    // 开始搜索
//                    // start search
//                    bluetoothManager.startDiscovery();
//        }  catch(BluetoothBLEException e) {
//                    e.printstackTrace();
//        }
//    }
//}
