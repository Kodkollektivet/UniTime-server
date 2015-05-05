import controller.MainViewController;
import javafx.application.Application;
import javafx.fxml.FXMLLoader;
import javafx.geometry.Rectangle2D;
import javafx.scene.Parent;
import javafx.scene.Scene;
import javafx.stage.Screen;
import javafx.stage.Stage;

/**
 * Created by otto on 2015-05-03.
 */
public class Main extends Application
{

    @Override
    public void start(Stage primaryStage) throws Exception {

        FXMLLoader fxmlLoader = new FXMLLoader(getClass().getResource("/assets/MainView.fxml"));
        Parent root;
        try {
            root = fxmlLoader.load();
            Rectangle2D visualBounds = Screen.getPrimary().getVisualBounds();
            Scene scene = new Scene(root);
            MainViewController mainViewController = fxmlLoader.getController();
            mainViewController.setStageSize((int) visualBounds.getHeight(), (int) visualBounds.getWidth());
            mainViewController.setStage(primaryStage);
            primaryStage.setScene(scene);
            primaryStage.setTitle("UniTime");
            primaryStage.show();
        } catch(Exception e) {
            e.printStackTrace();
        }
    }

    public static void main(String[] args) {
        launch(args);
    }
}
