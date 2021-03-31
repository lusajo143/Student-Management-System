package sample;

import javafx.application.Platform;
import javafx.beans.property.SimpleStringProperty;
import javafx.collections.FXCollections;
import javafx.collections.ObservableList;
import javafx.scene.control.Alert;
import javafx.scene.control.Label;
import javafx.scene.control.TableColumn;
import javafx.scene.control.TableView;
import javafx.scene.control.cell.PropertyValueFactory;
import javafx.scene.layout.StackPane;
import netscape.javascript.JSObject;
import org.json.JSONArray;
import org.json.JSONObject;
import sample.instructor.Present;

import java.io.*;
import java.net.Socket;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;
import java.text.DecimalFormat;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Date;

public class publicClass {

    private Label percent;
    private StackPane wait;
    private Label res_acc, res_loss, res_time, id;
    static ObservableList<Present> lists;

    public Socket socket() throws IOException {
        Socket socket = new Socket("127.0.0.1",143);
        return socket;
    }
    
    public publicClass(StackPane wait, Label res_acc,
                       Label res_loss, Label res_time, Label id){
        this.wait = wait;
        this.res_acc = res_acc;
        this.res_loss = res_loss;
        this.res_time = res_time;
        this.id = id;
    }

    public publicClass(Label percent) {
        this.percent = percent;
    }

    public publicClass(){

    }


    /*
    ** Returning connection from database
     */
    public Connection connection() throws ClassNotFoundException, SQLException {
        Class.forName("com.mysql.jdbc.Driver");
        return DriverManager.getConnection("jdbc:mysql://localhost/sams" ,
                "root","");
    }

    /*
    * Send all requests to the python server
    *
    * Boolean first is for checking is the request is for registering a student
    * so as to launch camera from Server
    *
     */
    public void send_msg(String msg, boolean first){
        new Thread(() -> {
            try {
                Socket socket = socket();
                if (socket.isConnected()) {
                    DataOutputStream outputStream = new DataOutputStream(socket.getOutputStream());
                    outputStream.writeUTF(msg);
                    outputStream.flush();

                    if (first) {
                        outputStream.writeUTF("a###start_camera");
                        outputStream.flush();
                        listen_(socket);
                    }
                    outputStream.close();
                    socket.close();
                }
            }catch (Exception e) {

            }
        }).start();
    }

    /*
    *
    * Sending train request to the Server
    * and Waits for feedback i.e loss and accuracy of the model
    *
     */
    public void train(String msg){
        new Thread(() -> {
            try {
                Socket socket = socket();
                if (socket.isConnected()) {
                    DataOutputStream outputStream = new DataOutputStream(socket.getOutputStream());
                    outputStream.writeUTF(msg);
                    outputStream.flush();

                    listen_(socket);
                    outputStream.close();
                    socket.close();
                }
            }catch (Exception e) {

            }
        }).start();
    }

    public Socket takeAttandance(String msg) throws IOException {

        Socket socket = socket();
        new Thread(() -> {
            try {

                if (socket.isConnected()) {
                    DataOutputStream outputStream = new DataOutputStream(socket.getOutputStream());
                    outputStream.writeUTF(msg);
                    outputStream.flush();

                    return;
                }
            }catch (Exception e) {

            }
        }).start();
        return socket;
    }

    public void stopAttendance(Socket socket, TableView tableView, TableColumn<Present, String> reg,
                               TableColumn<Present, String> acc){
        new Thread(() -> {
            try {
                DataOutputStream outputStream = new DataOutputStream(socket.getOutputStream());
                outputStream.writeUTF("a###stop");
                outputStream.flush();

                listen_attendance(socket,tableView, reg, acc);
                outputStream.close();
                socket.close();
            } catch (IOException e) {
                e.printStackTrace();
            }
        }).start();
    }

    /*
    *
    * Update percent label in admin panel when taking student face images
    *
     */
    public void setPercent(String value){
        percent.setText(value);
    }

    /*
    *
    * Update Result values in admin panel after training
    *
     */
    public void setTrain(String loss, String accuracy) {
        Date date = new Date();
        SimpleDateFormat format = new SimpleDateFormat("HH:mm  MMM dd, yyyy");
        Long time = date.getTime();
        res_time.setText(format.format(time));
        res_acc.setText(accuracy);
        res_loss.setText(loss);
        id.setText(String.valueOf(time));
    }

    public void listen_attendance(Socket socket, TableView tableView, TableColumn<Present, String> reg,
                                  TableColumn<Present, String> accuracy) throws IOException {
        BufferedReader reader = new BufferedReader(new InputStreamReader(socket.getInputStream()));
        String response = "";
        while ((response = reader.readLine()) != null) {
            if (percent != null) {
                String finalResponse = response;
                Platform.runLater(() -> {
                    setPercent(finalResponse);
                });
            } else if (wait != null) {
                wait.setVisible(false);
                String resp[] = response.split("###");
                Platform.runLater(() -> {
                    DecimalFormat format = new DecimalFormat("0.0000");
                    setTrain(format.format(Double.parseDouble(resp[0])),
                            format.format(Double.parseDouble(resp[1])));
                });
            } else {
                System.out.println(response);

                    JSONArray array = new JSONArray(response);
                    ObservableList<Present> list = FXCollections.observableArrayList();
                    lists = FXCollections.observableArrayList();

                    for (int i = 0; i < array.length(); i++) {
                        System.out.println(array.getJSONObject(i).getDouble("accuracy"));
                        list.add(new Present(array.getJSONObject(i).getString("reg"),
                                String.valueOf(array.getJSONObject(i).getDouble("accuracy"))));
                        lists.add(new Present(array.getJSONObject(i).getString("reg"),
                                String.valueOf(array.getJSONObject(i).getDouble("accuracy"))));
                    }
                    reg.setCellValueFactory(new PropertyValueFactory<>("Registration"));
                    accuracy.setCellValueFactory(new PropertyValueFactory<>("Accuracy"));
                if (tableView != null) {
                    tableView.setItems(list);
                } else {
                    System.out.println("null");
                }


                break;
            }
        }
    }

    /*
    * Listening for all kind of responses from the Server
    *
    * Different kinds of responses are identified by parameters or view they
    * are intended to update
    *
     */
    public void listen_(Socket socket) throws IOException {
        BufferedReader reader = new BufferedReader(new InputStreamReader(socket.getInputStream()));
        String response = "";
        while ((response = reader.readLine()) != null) {
            if (percent != null) {
                String finalResponse = response;
                Platform.runLater(() -> {
                    setPercent(finalResponse);
                });
            } else if (wait != null) {
                wait.setVisible(false);
                String resp[] = response.split("###");
                Platform.runLater(() -> {
                    DecimalFormat format = new DecimalFormat("0.0000");
                    setTrain(format.format(Double.parseDouble(resp[0])),
                            format.format(Double.parseDouble(resp[1])));
                });
            } else {
                System.out.println(response);
                break;
            }
        }
    }

    /*
    * Showing Warning alerts
     */
    public void alert(String title, String info){
        Alert alert = new Alert(Alert.AlertType.WARNING);
        alert.setHeaderText(title);
        alert.setContentText(info);
        alert.setTitle("");
        alert.show();
    }

    /*
    * Showing Information alerts
     */
    public void info(String title, String msg) {
        Alert alert = new Alert(Alert.AlertType.INFORMATION);
        alert.setContentText(msg);
        alert.setTitle("");
        alert.setHeaderText(title);
        alert.show();
    }

}
