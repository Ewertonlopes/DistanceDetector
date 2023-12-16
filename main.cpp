#include <iostream>
#include <opencv2/opencv.hpp>
 
using namespace std;
 
// Function for Face Detection
void detectAndDraw( cv::Mat& img, cv::CascadeClassifier& cascade, 
                cv::CascadeClassifier& nestedCascade, double scale );
string cascadeName, nestedCascadeName;
 
int k = 0;

int main( int argc, const char** argv )
{
    // VideoCapture class for playing video for which faces to be detected
    cv::VideoCapture capture; 
    cv::Mat frame, image;
 
    // PreDefined trained XML classifiers with facial features
    cv::CascadeClassifier cascade, nestedCascade; 
    double scale=1;

    // Load classifiers from "opencv/data/haarcascades" directory 
    // nestedCascade.load( "../../haarcascade_eye_tree_eyeglasses.xml" ) ;
 
    // Change path before execution 
    cascade.load( "models/haarcascade_frontalface_alt.xml" ) ; 
 
    // Start Video..1) 0 for WebCam 2) "Path to Video" for a Local Video
    capture.open(0); 
    if( capture.isOpened() )
    {
        // Capture frames from video and detect faces
        cout << "Face Detection Started...." << endl;
        while(1)
        {
            capture >> frame;
            if( frame.empty() )
                break;
            
            cv::Mat frame1 = frame.clone();
            detectAndDraw( frame1, cascade, nestedCascade, scale ); 
            char c = (char)cv::waitKey(10);
         
            // Press q to exit from window
            if( c == 27 || c == 'q' || c == 'Q' ) 
                break;
        }
    }
    else
        cout<<"Could not Open Camera";
    return 0;
}
 
void detectAndDraw( cv::Mat& img, cv::CascadeClassifier& cascade,
                    cv::CascadeClassifier& nestedCascade,
                    double scale)
{
    vector<cv::Rect> faces, faces2;
    cv::Mat gray, smallImg;
 
    cv::cvtColor( img, gray, cv::COLOR_BGR2GRAY ); // Convert to Gray Scale
    double fx = 1 / scale;

    cv::Mat filtered;
    cv::GaussianBlur(gray, filtered, cv::Size(5, 5), 2.0, 2.0);
 
    // Resize the Grayscale Image 
    cv::resize( filtered, smallImg, cv::Size(), fx, fx, cv::INTER_LINEAR ); 
    cv::equalizeHist( smallImg, smallImg );
 
    // Detect faces of different sizes using cascade classifier 
    cascade.detectMultiScale( smallImg, faces, 1.1, 
                            2, 0|cv::CASCADE_SCALE_IMAGE, cv::Size(24, 24) );
 
    // Draw circles around the faces
    for ( size_t i = 0; i < faces.size(); i++ )
    {
        cv::Rect r = faces[i];
        
        vector<cv::Rect> nestedObjects;
        cv::Point center;
        cv::Scalar color = cv::Scalar(255, 0, 0); // Color for Drawing tool
        int radius;
 
        double aspect_ratio = (double)r.width/r.height;
        if( 0.95 < aspect_ratio && aspect_ratio < 1.05 )
        {
            cv::Mat faceROI = img(r);
            std::stringstream filename;
            filename << "res/face_" << k++ << ".jpg";
            cv::imwrite(filename.str(),faceROI);
            center.x = round((r.x + r.width*0.5)*scale);
            center.y = round((r.y + r.height*0.5)*scale);
            radius = round((r.width + r.height)*0.25*scale);
            cv::circle( img, center, radius, color, 3, 8, 0 );
        }
        else
            cv::rectangle( img, cv::Point(round(r.x*scale), round(r.y*scale)),
                    cv::Point(round((r.x + r.width-1)*scale), 
                    round((r.y + r.height-1)*scale)), color, 3, 8, 0);
    }
 
    // Show Processed Image with detected faces
    cv::imshow( "Face Detection", img );
}