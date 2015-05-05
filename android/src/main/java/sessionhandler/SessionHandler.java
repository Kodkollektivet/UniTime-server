package sessionhandler;


import com.fasterxml.jackson.databind.ObjectMapper;
import model.Course;
import model.Event;
import org.apache.http.HttpEntity;
import org.apache.http.HttpResponse;
import org.apache.http.client.HttpClient;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.entity.StringEntity;
import org.apache.http.impl.client.HttpClientBuilder;
import org.apache.http.util.EntityUtils;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.MalformedURLException;
import java.net.URL;
import java.util.ArrayList;


/**
 * Created by otto on 2015-05-05.
 */
public class SessionHandler {

    public ArrayList<Course> courseInfoArrayList = new ArrayList<>();
    public ArrayList<Event> eventsArrayList = new ArrayList<>();

    // Empty contructor
    public SessionHandler() {}

    public void getAllCourses() {


        try {
            Course[] courseList;
            String urlName = "http://unitime.se:8000/api/course/";
            URL url = new URL(urlName);
            HttpURLConnection httpURLConnection = (HttpURLConnection) url.openConnection();

            ObjectMapper mapper = new ObjectMapper();

            httpURLConnection.setRequestMethod("GET");
            httpURLConnection.setRequestProperty("User-Agent", "UniTime-Android-Client");

            int responseCore = httpURLConnection.getResponseCode();

            //System.out.println("Sending 'GET' request to UTL : " + url.toString());
            System.out.println("Responsecode : " + responseCore);

            BufferedReader bufferedReader = new BufferedReader(new InputStreamReader(httpURLConnection.getInputStream()));
            String inputLine;
            StringBuilder response = new StringBuilder();

            while ((inputLine = bufferedReader.readLine()) != null){
                response.append(inputLine);
            }

            courseList = mapper.readValue(response.toString(), Course[].class);
            for (Course c : courseList) {
                courseInfoArrayList.add(c);
            }

        }
        catch (MalformedURLException e){
            e.printStackTrace();
        }
        catch (IOException e){
            e.printStackTrace();
        }



    }

    public void getEventsFromCourse(String courseCode) {

        HttpClient httpClient = HttpClientBuilder.create().build();

        try {
            Event[] eventList;
            String urlName = "http://unitime.se:8000/api/event/";
            ObjectMapper mapper = new ObjectMapper();
            String params = "course=" + courseCode;

            HttpPost request = new HttpPost(urlName);

            request.addHeader("User-Agent", "UniTime-Android-Client");
            request.addHeader("Accept", "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8");
            request.addHeader("Content-Type", "application/x-www-form-urlencoded");
            request.setEntity(new StringEntity(params));
            HttpResponse response = httpClient.execute(request);
            HttpEntity entity = response.getEntity();

            String content = EntityUtils.toString(entity);
            //String content = EntityUtils.toString(entity);
            //System.out.println(content);

            eventList = mapper.readValue(content, Event[].class);
            for (Event e : eventList) {
                eventsArrayList.add(e);
            }

        }
        catch (MalformedURLException e){
            e.printStackTrace();
        }
        catch (IOException e){
            e.printStackTrace();
        }



    }
}