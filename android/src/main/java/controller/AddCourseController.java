package controller;

import javafx.fxml.FXML;
import javafx.scene.control.Button;
import javafx.scene.control.ListView;
import javafx.scene.control.TextField;
import javafx.scene.image.ImageView;
import javafx.scene.layout.GridPane;
import javafx.scene.layout.VBox;
import sessionhandler.SessionHandler;

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

    public void setStageSize(int height, int width) {
        this.vboxMain.setPrefSize(width, height);
    }

    public ListView getAddedCoursesList() {
        return this.addedCoursesList;
    }

    @FXML
    private void onGetCourseClicked(){
        SessionHandler sh = new SessionHandler();
        sh.getEventsFromCourse(courseCodeTextField.getText());
        addedCoursesList.getItems().add(courseCodeTextField.getText());
    }


}
