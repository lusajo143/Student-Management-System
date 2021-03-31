package sample.admin;

import javafx.event.ActionEvent;
import javafx.fxml.FXML;
import javafx.fxml.FXMLLoader;
import javafx.scene.Parent;
import javafx.scene.control.TextField;
import javafx.scene.layout.BorderPane;
import sample.publicClass;

import java.io.IOException;
import java.sql.Connection;
import java.sql.SQLException;
import java.sql.Statement;

public class AdMain {
    @FXML
    BorderPane border;
    @FXML
    TextField stf_fname, stf_lname, stf_uname;


    public void std_(ActionEvent actionEvent) throws IOException {
        FXMLLoader loader = new FXMLLoader(getClass().getResource("stdnt.fxml"));
        Parent parent = loader.load();
        border.setCenter(parent);
    }

    public void stf_(ActionEvent actionEvent) throws IOException {
        FXMLLoader loader = new FXMLLoader(getClass().getResource("staff.fxml"));
        Parent parent = loader.load();
        border.setCenter(parent);
    }

    public void add_stf(ActionEvent actionEvent) throws SQLException, ClassNotFoundException {
        if (stf_fname.getText().equals("") || stf_lname.getText().equals("")
                || stf_uname.getText().equals("")) {
            new publicClass().alert("Error","Fill all fields");
        } else {
            String fname = stf_fname.getText();
            String lname = stf_lname.getText();
            String uname = stf_uname.getText();

            Connection con = new publicClass().connection();
            Statement sts = con.createStatement();
            sts.executeUpdate("insert into users values (null,'"+uname+"','"+fname+"','"+lname+"','"+lname.toUpperCase()+"','user');");

            new publicClass().info("Message",uname+" is successfully registered to the system.");

            stf_uname.setText("");
            stf_fname.setText("");
            stf_lname.setText("");

        }
    }

    public void train_(ActionEvent actionEvent) throws IOException {
        FXMLLoader loader = new FXMLLoader(getClass().getResource("train.fxml"));
        Parent parent = loader.load();
        border.setCenter(parent);
    }
}
