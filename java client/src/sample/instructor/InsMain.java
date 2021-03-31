package sample.instructor;

import javafx.beans.property.ReadOnlyObjectWrapper;
import javafx.beans.property.SimpleStringProperty;
import javafx.collections.FXCollections;
import javafx.collections.ObservableArray;
import javafx.collections.ObservableList;
import javafx.event.ActionEvent;
import javafx.fxml.FXML;
import javafx.scene.control.Button;
import javafx.scene.control.TableColumn;
import javafx.scene.control.TableView;
import javafx.scene.control.cell.PropertyValueFactory;
import sample.publicClass;

import java.io.IOException;
import java.net.Socket;
import java.sql.Connection;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import java.util.Date;


public class InsMain {
    @FXML
    Button attendance;
    Socket socket;

    @FXML
    TableColumn<Present, String> column_present;
    @FXML
    TableColumn<Present, String> column_acc;
    @FXML
    TableView table_present;

    public void start(ActionEvent actionEvent) throws SQLException, ClassNotFoundException, IOException {
        if (attendance.getText().equals("Start") || socket == null) {
            Connection con = new publicClass().connection();
            Statement sts = con.createStatement();
            ResultSet rs = sts.executeQuery("select time from models;");
            if (rs.last()) {
                Date date = new Date();
                socket = new publicClass().takeAttandance("a###attendance###"+date.getTime()+"###"+rs.getString(1));
            }
            attendance.setText("Stop");
        } else {
            attendance.setText("Start");
            if (socket.isConnected()) {
                new publicClass().stopAttendance(socket, table_present, column_present, column_acc);
            }
        }

    }

}
