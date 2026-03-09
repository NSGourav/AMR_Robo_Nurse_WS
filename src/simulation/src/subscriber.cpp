#include<iostream>

#include "rclcpp/rclcpp.hpp"
#include "std_msgs/msg/string.hpp"

class MYsubscriber : public rclcpp::Node{

    public:
     MYsubscriber() : Node("listnere"){

        subscriber_= this->create_subscription<std_msgs::msg::String>("TOPIC", 10 , std::bind(&MYsubscriber::topic_callback, this, std::placeholders::_1));
        RCLCPP_INFO(this->get_logger(), "Listening to topic HI");
     }

     private:
      void topic_callback(std_msgs::msg::String::SharedPtr msg){
         RCLCPP_INFO(this->get_logger(), "'%s'", msg->data.c_str());
      }

   rclcpp::Subscription<std_msgs::msg::String>::SharedPtr subscriber_;

};

int main(int argv , char *argc[]){

   rclcpp::init( argv , argc);
   rclcpp::spin(std::make_shared<MYsubscriber>());
   rclcpp::shutdown();
   return 0;
}