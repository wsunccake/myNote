package chapter14.example;

import javafx.application.Application;
import javafx.scene.control.Button;
import javafx.scene.Scene;
import javafx.stage.Stage;

import java.awt.*;

public class MyJavaFX extends Application {

    @Override
    public void start(Stage primaryStage) throws Exception {
        Button btnOK = new Button("OK");
        Scene scene = new Scene(btnOK, 200, 50);
        primaryStage.setTitle("MyJavaFX");
        primaryStage.setScene(scene);
        primaryStage.show();
    }

    public static void main(String[] args) {
        Application.launch();
    }
}
