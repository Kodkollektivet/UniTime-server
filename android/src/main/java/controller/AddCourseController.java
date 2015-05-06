package controller;

import javafx.fxml.FXML;
import javafx.fxml.FXMLLoader;
import javafx.scene.Parent;
import javafx.scene.control.Button;
import javafx.scene.control.ListView;
import javafx.scene.control.TextField;
import javafx.scene.image.ImageView;
import javafx.scene.layout.GridPane;
import javafx.scene.layout.VBox;
import model.Event;
import sessionhandler.SessionHandler;

import java.io.IOException;

/**
 * Created by otto on 2015-05-05.
 */
public class AddCourseController {


    @FXML
    private TextField courseCodeTextField;

    @FXML
    private Button addCourseBtn;

    @FXML
    private ListView<String> addedCoursesList;

    @FXML
    private ImageView goBackBtn;

    @FXML
    private GridPane addCourseGridpane;

    @FXML
    private VBox vboxMain;

    public ListView eventList;



    public void setStageSize(int height, int width) {
        this.vboxMain.setPrefSize(width, height);
    }

    public ListView getAddedCoursesList() {
        return this.addedCoursesList;
    }

    @FXML
    private void onGetCourseClicked(){
        if (!addedCoursesList.getItems().contains(courseCodeTextField.getText()) &&
                !courseCodeTextField.getText().isEmpty()) {
            SessionHandler sh = new SessionHandler();
            sh.getEventsFromCourse(courseCodeTextField.getText());
            for (Event e : sh.eventsArrayList) {
                addEventToList(e);
            }
            addedCoursesList.getItems().add(courseCodeTextField.getText().toUpperCase());
        }
    }

    @FXML
    private void onGoBackClicked() {
        MainViewController.stage.setScene(MainViewController.mainScene);
    }

    public void addEventToList(Event event) {

        FXMLLoader fxmlLoader = new FXMLLoader(getClass().getResource("/assets/EventView.fxml"));
        Parent root = null;
        try {
            root = fxmlLoader.load();
            EventController eventController = fxmlLoader.getController();
            eventController.getEventInfoLabel().setText(event.getInfo());
            eventController.getEventRoomLabel().setText(event.getRoom());
            eventController.getEventTeacherLabel().setText(event.getTeacher());
            eventController.getEventTimeLabel().setText(event.getStarttime() + "-" + event.getEndtime());
            eventController.getEventStackPane().setStyle("-fx-background-color: red;");
            eventList.getItems().add(root);
        } catch (IOException e) {
            e.printStackTrace();
        }
    }


}
