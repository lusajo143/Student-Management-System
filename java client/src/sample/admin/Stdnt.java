package sample.admin;

import javafx.event.ActionEvent;
import javafx.fxml.FXML;
import javafx.scene.control.Label;
import javafx.scene.control.TextField;
import sample.publicClass;

public class Stdnt {

    @FXML
    TextField std_reg, std_fname, std_lname, std_course;
    @FXML
    Label cent;

    public void launch_cam(ActionEvent actionEvent) {
        new publicClass(cent).send_msg("aa###name###"+std_reg.getText(),true);
    }
}
