package sample.instructor;


public class Present{
    String Registration;
    String Accuracy;

    public Present(String registration, String accuracy) {
        Registration = registration;
        Accuracy = accuracy;
    }

    public String getRegistration() {
        return Registration;
    }

    public String getAccuracy() {
        return Accuracy;
    }

    public void setRegistration(String registration) {
        Registration = registration;
    }

    public void setAccuracy(String accuracy) {
        Accuracy = accuracy;
    }
}
