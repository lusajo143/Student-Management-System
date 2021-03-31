package sample;

import javafx.event.ActionEvent;
import javafx.fxml.FXML;
import javafx.fxml.FXMLLoader;
import javafx.scene.Parent;
import javafx.scene.Scene;
import javafx.scene.control.PasswordField;
import javafx.scene.control.TextField;
import javafx.scene.layout.BorderPane;
import javafx.stage.Stage;

import java.io.IOException;
import java.sql.Connection;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;

public class Controller {

    @FXML
    TextField username;
    @FXML
    PasswordField password;


    public void done_(ActionEvent actionEvent) throws SQLException, ClassNotFoundException, IOException {
        if (username.getText().equals("") || password.getText().equals("")) {
            new publicClass().alert("Error","Both Username and Password must not be empty");
        } else {
            String uName = username.getText();
            String pWord = password.getText();

            Connection connection = new publicClass().connection();
            Statement sts = connection.createStatement();
            ResultSet rs = sts.executeQuery("select * from users where username='"+uName+"' and password='"+pWord+"';");

            if (rs.next()) {
                String role = rs.getString("role");
                if (role.equals("admin")) {
                    FXMLLoader loader = new FXMLLoader(getClass().getResource("admin/ad_main.fxml"));
                    Parent parent = loader.load();

                    Stage stage = (Stage) password.getScene().getWindow();
                    stage.setScene(new Scene(parent,1000,600));
                } else {
                    FXMLLoader loader = new FXMLLoader(getClass().getResource("instructor/ins_main.fxml"));
                    Parent parent = loader.load();

                    Stage stage = (Stage) password.getScene().getWindow();
                    stage.setScene(new Scene(parent,1000,600));
                }
            } else {
                new publicClass().alert("Error","Wrong username or password");
            }

        }
    }
}
