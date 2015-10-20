package chapter14.example;

import javafx.application.Application;
import javafx.scene.Scene;
import javafx.scene.layout.StackPane;
import javafx.scene.text.Text;
import javafx.stage.Stage;

public class HelloJavaFX extends Application{
    @Override
    public void start(Stage primaryStage) throws Exception {
        StackPane pane = new StackPane();
        Text text = new Text("Hello JavaFX");
        pane.getChildren().add(text);
        pane.setPrefSize(200, 100);
        Scene scene = new Scene(pane);
        primaryStage.setTitle("Hi");
        primaryStage.setScene(scene);
        primaryStage.show();
    }
}
