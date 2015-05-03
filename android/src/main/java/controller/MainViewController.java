package controller;

import javafx.fxml.FXML;
import javafx.scene.control.Button;
import javafx.scene.control.TextField;
import javafx.scene.image.ImageView;
import javafx.scene.layout.VBox;


/**
 * Created by otto on 2015-05-03.
 */
public class MainViewController {

    @FXML
    private TextField courseCodeTF;

    @FXML
    private Button getCourseBtn;

    @FXML
    private VBox vboxMain;

    @FXML
    private ImageView updateCoursesMain;

    @FXML
    private ImageView addCoursesMain;


    public void setStageSize(int height, int width) {
        this.vboxMain.setPrefSize(width, height);
    }

    @FXML
    private void onUpdateClicked() {
        courseCodeTF.setText("Updated");
    }

    @FXML
    private void onAddClicked() {
        courseCodeTF.setText("Course Added");
    }

    @FXML
    private void onGetClicked() {
        courseCodeTF.setText("Getting Course");
    }
}


