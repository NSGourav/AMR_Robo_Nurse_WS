#include<iostream>
#include "rclcpp/rclcpp.hpp"

#include "std_msgs/msg/string.hpp"

class MypublisherNode : public rclcpp::Node{
    
    public:
     MypublisherNode() : Node("Publisher_Node"){
        publisher_ = this->create_publisher<std_msgs::msg::String>("HI",10);
        timer_ = this->create_wall_timer(
            std::chrono::seconds(1),
            std::bind(&MypublisherNode::publish_msg, this));
            RCLCPP_INFO(this->get_logger(), "Publisher node has been started.");
    }

    private:
     void publish_msg(){
        auto msg = std_msgs::msg::String();
        msg.data = "HI THIS IS MOHIT";
        publisher_ ->publish(msg);

    }

    rclcpp::Publisher<std_msgs::msg::String>::SharedPtr publisher_;
    rclcpp::TimerBase::SharedPtr timer_;
};

int main(int argc, char *argv[]) {
    rclcpp::init(argc, argv);
    rclcpp::spin(std::make_shared<MypublisherNode>());
    rclcpp::shutdown();
    return 0;
}