package sample.admin;

import javafx.application.Platform;
import javafx.event.ActionEvent;
import javafx.fxml.FXML;
import javafx.scene.control.Label;
import javafx.scene.layout.StackPane;
import sample.publicClass;

import java.sql.Connection;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;

public class Train {

    @FXML
    StackPane wait;
    @FXML
    Label res_date, res_acc, res_loss, id, cur_date, cur_acc, cur_loss;


    public void train_(ActionEvent actionEvent) {
        wait.setVisible(true);
        new publicClass(wait, res_acc, res_loss, res_date, id).train("a###start_train");
    }

    public void save_(ActionEvent actionEvent) throws SQLException, ClassNotFoundException {
        if (!id.getText().equals("id")) {
            Connection conn = new publicClass()
                    .connection();

            Statement sts = conn.createStatement();
            ResultSet rs = sts.executeQuery("select * from models where time='"+id.getText()+"';");

            if (rs.next()) {
                new publicClass().info("Message","Already saved");
            } else {
                sts.executeUpdate("insert into models values (null,'"+id.getText()+"','"+res_acc.getText()+"','"+res_loss.getText()+"');");
                new publicClass().send_msg("a###save###"+id.getText(),false);
                id.setText("id");
                cur_acc.setText(res_acc.getText());
                cur_loss.setText(res_loss.getText());
                cur_date.setText(res_date.getText());
                res_acc.setText("0.0000");
                res_loss.setText("0.0000");
                res_date.setText("                               .");
                new publicClass().info("Message","Done saving");
            }

        }
    }
}
