package com.example.client_containment.Service;

import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.content.SharedPreferences;
import android.location.Location;
import android.util.Log;
import android.widget.Toast;

import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.JsonArrayRequest;
import com.android.volley.toolbox.JsonObjectRequest;
import com.android.volley.toolbox.RequestFuture;
import com.android.volley.toolbox.Volley;
import com.example.client_containment.MainActivity;
import com.google.android.gms.location.LocationResult;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.util.ArrayList;
import java.util.Calendar;
import java.util.List;


public class MyLocationService extends BroadcastReceiver {

    public static final String ACTION_PROCESS_UPDATE = "com.example.client_containment.Service.UPDATE_LOCATION";
    ArrayList<Location> locationListG = new ArrayList<>();
    @Override
    public void onReceive(Context context, Intent intent) {
        if(intent != null){
            final String action = intent.getAction();
            if(ACTION_PROCESS_UPDATE.equals(action)){
                LocationResult result = LocationResult.extractResult(intent);
                if(result != null){
                    Location location = result.getLastLocation();
                    String loc = new StringBuilder(String.valueOf(location.getLatitude()))
                            .append("/")
                            .append(location.getLongitude())
                            .toString();

                    try {
                        MainActivity.getInstance().updateTextView(loc);
                        postDataUsingVolley(Double.toString(location.getLatitude()),Double.toString(location.getLongitude()),context);
                        getDataUsingVolley(context,location);
                        Toast.makeText(context, loc, Toast.LENGTH_SHORT).show();
                    }catch (Exception ex){
                        Toast.makeText(context,loc,Toast.LENGTH_SHORT).show();
                        postDataUsingVolley(Double.toString(location.getLatitude()),Double.toString(location.getLongitude()),context);
                    }
                }
            }
        }

    }

    private void getDataUsingVolley(Context context,Location location) {
        SharedPreferences sharedPreferences = context.getSharedPreferences("user_data", 0);;
        ArrayList<Location> locationList = new ArrayList<>();
        final RequestQueue queue = Volley.newRequestQueue(context);
        RequestFuture<JSONArray> requestFuture= RequestFuture.newFuture();
        String url = "http://192.168.43.234:5000/location_data";
        JsonArrayRequest jsonObjReq = new JsonArrayRequest(Request.Method.GET, url, null,
                response -> {
                    for (int locationIndex = 0; locationIndex < response.length(); locationIndex++) {
                        try {
                            JSONObject j = response.getJSONObject(locationIndex);
                            Location l = new Location("");
                            l.setLatitude(new Double(j.getString("LOCATE_LAT")));
                                l.setLongitude(new Double(j.getString("LOCATE_LANG")));
                            int locationId = j.getInt("LOCATE_ID");
                            Double latitude  = Double.parseDouble(sharedPreferences.getString("visited","0"));
                            Double longitude = Double.parseDouble(sharedPreferences.getString("visited","0"));
                            Location alreadyVisited = new Location("");
                            alreadyVisited.setLongitude(longitude);
                            alreadyVisited.setLatitude(latitude);
                            if(l.distanceTo(alreadyVisited) != 0){
                                float distanceInMeters = l.distanceTo(location);
                                Log.d("dis",String.valueOf(distanceInMeters));
                                if(distanceInMeters < 100){
//                                    create a toast message to warn the user
                                    Toast.makeText(context,"You are near a location with covid-19 cases",Toast.LENGTH_LONG).show();
                                    sendMailUsingVolley(context,locationId);
                                    SharedPreferences.Editor editor = sharedPreferences.edit();
                                    editor.putString("latitudeVisited", Double.toString(l.getLatitude()));
                                    editor.putString("longitudeVisited", Double.toString(l.getLongitude()));
                                    editor.commit();
                                }
                            }
                        } catch (JSONException e) {
                            e.printStackTrace();
                        }
                    }
                },
                error -> Log.d("error",error.toString()));
        Log.d("list",locationList.toString());
        queue.add(jsonObjReq);
    }
    private void postDataUsingVolley(String lat,String lon,Context context) {
        final RequestQueue queue = Volley.newRequestQueue(context);
        String url = "http://192.168.43.234:5000/post_user_location_data";
        SharedPreferences sharedPreferences = context.getSharedPreferences("user_data", 0);
        int id = sharedPreferences.getInt("id",0);
        JSONObject postparams = new JSONObject();
        try {
            postparams.put("id", id);
            postparams.put("lat", lat);
            postparams.put("long",lon);
            postparams.put("timestamp", Calendar.getInstance().getTime().toString());
        } catch (JSONException e) {
            e.printStackTrace();
        }

        JsonObjectRequest jsonObjReq = new JsonObjectRequest(Request.Method.POST, url, postparams,
                response -> Log.d("response",response.toString()),
                error -> Log.d("error",error.toString()));

        queue.add(jsonObjReq);
    }

    private void sendMailUsingVolley(Context context,int locationId) {
        final RequestQueue queue = Volley.newRequestQueue(context);
        String url = "http://192.168.43.234:5000/send_trigger";
        SharedPreferences sharedPreferences = context.getSharedPreferences("user_data", 0);
//        getting user email from shared preferences
        String email = sharedPreferences.getString("email","");
        JSONObject postparams = new JSONObject();
        System.out.println("The email is : "+email);
        try {
            postparams.put("email", email);
            postparams.put("id", locationId);
        } catch (JSONException e) {
            e.printStackTrace();
        }



        JsonObjectRequest jsonObjReq = new JsonObjectRequest(Request.Method.POST, url, postparams,

                response -> Log.d("response",response.toString()),
                error -> Log.d("error",error.toString()));

        queue.add(jsonObjReq);
    }
}