package chapter14.example;

import javafx.application.Application;
import javafx.scene.Scene;
import javafx.scene.control.Button;
import javafx.stage.Stage;

public class MultipleStageDemo extends Application{

    @Override
    public void start(Stage primaryStage) throws Exception {
        Scene scene = new Scene(new Button("OK"), 150, 50);
        primaryStage.setScene(scene);
        primaryStage.setTitle("MyJavaFX");
        primaryStage.show();

        Stage stage = new Stage();
        stage.setTitle("Second stage");
        stage.setScene(new Scene(new Button("New Stage"), 180, 100));
        stage.show();
    }

    public static void main(String[] args) {
        Application.launch();
    }
}
