package sample.admin;

import javafx.event.ActionEvent;
import javafx.fxml.FXML;
import javafx.scene.control.TextField;
import sample.publicClass;

import java.sql.Connection;
import java.sql.SQLException;
import java.sql.Statement;

public class Staff {

    @FXML
    TextField stf_fname2, stf_lname2, stf_uname2;


    public void stf2_(ActionEvent actionEvent) throws SQLException, ClassNotFoundException {

        if (stf_fname2.getText().equals("") || stf_lname2.getText().equals("")
                || stf_uname2.getText().equals("")) {
            new publicClass().alert("Error","Fill all fields");
        } else {
            String fname = stf_fname2.getText();
            String lname = stf_lname2.getText();
            String uname = stf_uname2.getText();

            Connection con = new publicClass().connection();
            Statement sts = con.createStatement();
            sts.executeUpdate("insert into users values (null,'"+uname+"','"+fname+"','"+lname+"','"+lname.toUpperCase()+"','user');");

            new publicClass().info("Message",uname+" is successfully registered to the system.");

            stf_uname2.setText("");
            stf_fname2.setText("");
            stf_lname2.setText("");

        }

    }
}
