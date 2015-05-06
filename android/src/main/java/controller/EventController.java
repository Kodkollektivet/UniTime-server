package controller;

import javafx.fxml.FXML;
import javafx.scene.control.Label;
import javafx.scene.layout.StackPane;

/**
 * Created by otto on 2015-05-06.
 */
public class EventController {

    @FXML
    private Label eventTeacherLabel;

    @FXML
    private Label eventInfoLabel;

    @FXML
    private Label eventRoomLabel;

    @FXML
    private Label eventTimeLabel;

    @FXML
    private StackPane eventStackPane;


    public Label getEventTeacherLabel() {
        return eventTeacherLabel;
    }

    public void setEventTeacherLabel(Label eventTeacherLabel) {
        this.eventTeacherLabel = eventTeacherLabel;
    }

    public Label getEventInfoLabel() {
        return eventInfoLabel;
    }

    public void setEventInfoLabel(Label eventInfoLabel) {
        this.eventInfoLabel = eventInfoLabel;
    }

    public Label getEventRoomLabel() {
        return eventRoomLabel;
    }

    public void setEventRoomLabel(Label eventRoomLabel) {
        this.eventRoomLabel = eventRoomLabel;
    }

    public Label getEventTimeLabel() {
        return eventTimeLabel;
    }

    public void setEventTimeLabel(Label eventTimeLabel) {
        this.eventTimeLabel = eventTimeLabel;
    }

    public StackPane getEventStackPane() {
        return eventStackPane;
    }

    public void setEventStackPane(StackPane eventStackPane) {
        this.eventStackPane = eventStackPane;
    }
}
