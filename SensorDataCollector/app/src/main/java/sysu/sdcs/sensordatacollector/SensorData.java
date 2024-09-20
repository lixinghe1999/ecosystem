package sysu.sdcs.sensordatacollector;

import android.os.Environment;
import android.util.Log;

import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

/**
 * Created by justk on 2018/6/13.
 */

public class SensorData {
    public static List<String> timestamps = new ArrayList<String>();
    public static List<String[]> magneticSensorData = new ArrayList<String[]>();
    public static List<String[]> accelerometerSensorData = new ArrayList<String[]>();
    public static List<String[]> orientationSensorData = new ArrayList<String[]>();
    public static List<String[]> stepSensorData = new ArrayList<String[]>();
    public static List<String[]> gyroscopeSensorData = new ArrayList<String[]>();
    public static String file_path = Environment.getExternalStorageDirectory().getAbsolutePath()
            + "/SensorData/";
    private static FileWriter writer;

    public static File createFile(String file_name){
        File file = new File(file_path + file_name);
        try{
            if(!file.exists())
                file.createNewFile();

        }catch (IOException e ){
            Log.e("file create error", e.getMessage() );

        }
        return file;
    }

    public static void createFilePath(){
        try{
            File file = new File(file_path);
            if(!file.exists())
                file.mkdir();
        }
        catch(Exception e){
            Log.e("file path create error", e.getMessage() );

        }
    }
    public static void clear(){
        timestamps.clear();
        magneticSensorData.clear();
        accelerometerSensorData.clear();
        orientationSensorData.clear();
        stepSensorData.clear();
        gyroscopeSensorData.clear();

    }
    public static boolean init(String file_name) {
        createFilePath();
        try {
            writer = new FileWriter(createFile(file_name), true);
            String header = getFileHead();
            writer.append(header);
            writer.flush();
            return true;
        } catch (IOException e) {
            Log.e("file write error", e.getMessage() );
        }
        return false;
    }



    public static void addSensorData(String[] mData, String[] aData, String[] oData,
                                     String gData[], String[] sData, String captime){
        magneticSensorData.add(mData);
        accelerometerSensorData.add(aData);
        orientationSensorData.add(oData);
        stepSensorData.add(sData);
        gyroscopeSensorData.add(gData);
        timestamps.add(captime);
    }
    public static void addAccGyroData(String[] aData, String gData[], String captime){
        accelerometerSensorData.add(aData);
        gyroscopeSensorData.add(gData);
        timestamps.add(captime);

        Log.d("size of acc", ""+accelerometerSensorData.size());
        if (accelerometerSensorData.size() > 10){
            try {
                String data = "";
                for (int i = 0; i < accelerometerSensorData.size(); i++) {
                    String[] acc = accelerometerSensorData.get(i);
                    String[] gyro = gyroscopeSensorData.get(i);
                    String one_detail = ""
                            + acc[0] + "," + acc[1] + "," + acc[2] + ","
                            + gyro[0] + "," + gyro[1] + "," + gyro[2] + "," + timestamps.get(i) + "\n";
                    data += one_detail;
                }
                writer.append(data);
                writer.flush();
                accelerometerSensorData = new ArrayList<String[]>();
                gyroscopeSensorData = new ArrayList<String[]>();
                timestamps = new ArrayList<String>();
            } catch (IOException e) {
                Log.e("file write error", e.getMessage() );
            }
        }
    }
    public static boolean saveSensorData_batch(String file_name){
        createFilePath();
        try {
            FileWriter writer;
            writer = new FileWriter(createFile(file_name), true);
            Log.d("size of data", ""+accelerometerSensorData.size());
            for(int i = 0 ; i < accelerometerSensorData.size() ; i++){
                String[] acc = accelerometerSensorData.get(i);
                String[] gyro = gyroscopeSensorData.get(i);
                String one_detail = ""
                        + acc[0] + "," + acc[1] + "," + acc[2] + ","
                        + gyro[0] + "," + gyro[1] + "," + gyro[2] + "," + timestamps.get(i) + "\n" ;
                writer.append(one_detail);
                writer.flush();
            }
            writer.close();
            return true;
        } catch (IOException e) {
            Log.e("file write error", e.getMessage() );
        }
        return false;
    }

    public static String getFileHead(){
//        return  "frame,mag_x,mag_y,mag_z,acc_x,acc_y,acc_z,gyro_x,gyro_y,gyro_z," +
//                "orien_x,orien_y,orien_z,step_detect,step_count,timestamp\n";
        return  "acc_x,acc_y,acc_z,gyro_x,gyro_y,gyro_z,timestamp\n";
    }

    public static String getAllDataStr(){
        String data = "";
        for(int i = 0 ; i < magneticSensorData.size() ; i++){
            String[] mag = magneticSensorData.get(i);
            String[] gyro = gyroscopeSensorData.get(i);
            String[] orien = orientationSensorData.get(i);
            String[] step = stepSensorData.get(i);
            String[] acc = accelerometerSensorData.get(i);
            String one_detail = "" + (i+1) + ","
                    + mag[0] + "," + mag[1] + "," + mag[2] + ","
                    + acc[0] + "," + acc[1] + "," + acc[2] + ","
                    + gyro[0] + "," + gyro[1] + "," + gyro[2] + ","
                    + orien[0] + "," + orien[1] + "," + orien[2] + ","
                    + null2zero(step[0]) + "," + step[1] + "," + timestamps.get(i) + "\n" ;
            data = data + one_detail;
        }
//        clear();
        return data;
    }
    public static String getAccGyroDataStr(){
        String data = "";
        for(int i = 0 ; i < accelerometerSensorData.size() ; i++){
            String[] gyro = gyroscopeSensorData.get(i);
            String[] acc = accelerometerSensorData.get(i);
            String one_detail = ""
                    + acc[0] + "," + acc[1] + "," + acc[2] + ","
                    + gyro[0] + "," + gyro[1] + "," + gyro[2] + "," + timestamps.get(i) + "\n" ;
            data = data + one_detail;
        }
//        clear();
        return data;
    }

    public static String null2zero(String item){
        if(item == null || item.equals(""))
            return "0";
        return item;
    }

}
