package controller;

import javafx.fxml.FXML;
import javafx.fxml.FXMLLoader;
import javafx.geometry.Rectangle2D;
import javafx.scene.Parent;
import javafx.scene.Scene;
import javafx.scene.control.ListView;
import javafx.scene.image.ImageView;
import javafx.scene.layout.AnchorPane;
import javafx.scene.layout.GridPane;
import javafx.stage.Screen;
import javafx.stage.Stage;

import java.io.IOException;


/**
 * Created by otto on 2015-05-03.
 */
public class MainViewController {

    @FXML
    private ImageView updateCoursesMain;

    @FXML
    private ImageView addCoursesMain;

    @FXML
    private ListView eventList;

    @FXML
    private GridPane gridpaneMain;

    @FXML
    private AnchorPane anchorPaneMain;


    private Stage stage;


    public void setStageSize(int height, int width) {
        this.anchorPaneMain.setPrefSize(width, height);
    }

    @FXML
    private void onUpdateClicked() {

    }

    @FXML
    private void onAddCoursesClicked() {
        FXMLLoader fxmlLoader = new FXMLLoader(getClass().getResource("/assets/AddCourseView.fxml"));
        Parent root = null;
        try {
            root = fxmlLoader.load();
            Rectangle2D visualBounds = Screen.getPrimary().getVisualBounds();
            AddCourseController addCourseController = fxmlLoader.getController();
            addCourseController.setStageSize((int) visualBounds.getHeight(), (int) visualBounds.getWidth());
            getStage().setScene(new Scene(root));
        } catch (IOException e) {
            e.printStackTrace();
        }

    }

    public void setStage(Stage stage) {
        this.stage = stage;
    }

    public Stage getStage() {
        return this.stage;
    }

    public ListView getEventList() {
        return eventList;
    }

    public GridPane getGridpaneMain() {
        return gridpaneMain;
    }
}


