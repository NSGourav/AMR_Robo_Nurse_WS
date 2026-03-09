#include<iostream>
#include "rclcpp/rclcpp.hpp"
#include "std_msgs/msg/string.hpp"

class MYnode : public rclcpp::Node{

    public:
     MYnode() : Node("publisher_2"){
        publisher_ =this->create_publisher<std_msgs::msg::String()>("no",10);
        timer_ = this->create_wall_timer(
            std::chrono::seconds(1),
            std::bind(&MYnode::publish_function , this)  
        );
            RCLCPP_INFO(this->get_logger(), "Publisher node has started");
            
    }

    private:
     void publish_function(){
         auto msg = std_msgs::msg::String();
         msg.data = "THis is Node";
         publisher_ ->publish(msg);
     }

     rclcpp::Publisher<std_msgs::msg::String>::SharedPtr publisher_;
     rclcpp::TimerBase::SharedPtr timer_;
};

int main(int argc , char *argv[]){
    rclcpp::init(argc , argv);
    rclcpp::spin(std::make_shared<MYnode>());
    rclcpp::shutdown();
    return 0;



}