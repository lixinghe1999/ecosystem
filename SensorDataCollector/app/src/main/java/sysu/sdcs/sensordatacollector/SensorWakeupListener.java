package sysu.sdcs.sensordatacollector;
import android.hardware.SensorEvent;
import android.hardware.Sensor;
import android.hardware.SensorEventListener;
import android.util.Log;

public class SensorWakeupListener implements SensorEventListener {
        @Override
        public void onSensorChanged(SensorEvent event) {
            Log.i("wakeup", "change");
            // Handle wake-up event
        }

        @Override
        public void onAccuracyChanged(Sensor sensor, int accuracy) {
            // Handle accuracy change if needed
        }
}
