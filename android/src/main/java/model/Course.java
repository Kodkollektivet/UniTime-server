package model;

/**
 * Created by otto on 2015-05-05.
 */
public class Course {

    private String season;
    private String course_code;
    private String year;
    private String course_anmalningskod;
    private String html_url;
    private String model;
    private String pk;

    public String getSeason() {
        return season;
    }

    public void setSeason(String season) {
        this.season = season;
    }

    public String getCourse_code() {
        return course_code;
    }

    public void setCourse_code(String course_code) {
        this.course_code = course_code;
    }

    public String getYear() {
        return year;
    }

    public void setYear(String year) {
        this.year = year;
    }

    public String getCourse_anmalningskod() {
        return course_anmalningskod;
    }

    public void setCourse_anmalningskod(String course_anmalningskod) {
        this.course_anmalningskod = course_anmalningskod;
    }

    public String getHtml_url() {
        return html_url;
    }

    public void setHtml_url(String html_url) {
        this.html_url = html_url;
    }

    public String getModel() {
        return model;
    }

    public void setModel(String model) {
        this.model = model;
    }

    public String getPk() {
        return pk;
    }

    public void setPk(String pk) {
        this.pk = pk;
    }
}
