package model;

import java.time.LocalDate;

/**
 * Created by otto on 2015-05-03.
 */
public class Event implements Comparable<Event> {

    private String startdate;

    private String starttime;

    private String endtime;

    private String info;

    private String room;

    private String teacher;


    public String getStartdate() {
        return startdate;
    }

    public void setStartdate(String startdate) {
        this.startdate = startdate;
    }

    public String getStarttime() {
        return starttime;
    }

    public void setStarttime(String starttime) {
        this.starttime = starttime;
    }

    public String getEndtime() {
        return endtime;
    }

    public void setEndtime(String endtime) {
        this.endtime = endtime;
    }

    public String getTeacher() {
        return teacher;
    }

    public void setTeacher(String teacher) {
        this.teacher = teacher;
    }

    public String getInfo() {
        return info;
    }

    public void setInfo(String info) {
        this.info = info;
    }

    public String getRoom() {
        return room;
    }

    public void setRoom(String room) {
        this.room = room;
    }
    @Override
    public int compareTo(Event event) {
        return LocalDate.parse(this.startdate).compareTo(LocalDate.parse(event.startdate));
    }

}
