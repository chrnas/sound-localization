#include <sio_server.h>
#include <functional>
#include <iostream>
#include <map>
#include <string>
#include <chrono>

class AudioServer {
public:
    AudioServer(unsigned int port) : _port(port) {
        _server.set_open_listener(std::bind(&AudioServer::onConnected, this, std::placeholders::_1));
        _server.set_close_listener(std::bind(&AudioServer::onDisconnected, this, std::placeholders::_1));
        _server.set_fail_listener(std::bind(&AudioServer::onFailed, this));

        _server.bind_events();
    }

    void run() {
        _server.listen(_port);
    }

private:
    sio::server _server;
    unsigned int _port;
    std::map<std::string, std::pair<float, float>> _userPositions; // Store user positions

    void bind_events() {
        _server.on("newUser", sio::socket::event_listener_aux([&](std::string const& name, sio::message::ptr const& data, bool isAck,sio::message::list &ack_resp) {
            auto userName = data->get_map()["name"]->get_string();
            auto xCoordinate = data->get_map()["xCoordinate"]->get_double();
            auto yCoordinate = data->get_map()["yCoordinate"]->get_double();

            _userPositions[userName] = {xCoordinate, yCoordinate};

            std::cout << "New User: " << userName << " at (" << xCoordinate << ", " << yCoordinate << ")" << std::endl;
        }));

        _server.on("syncTime", sio::socket::event_listener_aux([&](std::string const& name, sio::message::ptr const& data, bool isAck,sio::message::list &ack_resp) {
            auto now = std::chrono::high_resolution_clock::now();
            auto now_ms = std::chrono::time_point_cast<std::chrono::milliseconds>(now);
            auto value = now_ms.time_since_epoch();
            long duration = value.count();

            ack_resp.push(sio::int_message::create(duration)); // Respond with the server timestamp
            std::cout << "Sync Time requested, responding with: " << duration << std::endl;
        }));

        _server.on("audioData", sio::socket::event_listener_aux([&](std::string const& name, sio::message::ptr const& data, bool isAck,sio::message::list &ack_resp) {
            auto audioData = data->get_map()["data"]->get_vector();
            auto timestamp = data->get_map()["timestamp"]->get_double();

            std::cout << "Received audio data with timestamp: " << timestamp << std::endl;
            // Process audio data as needed
        }));
    }

    void onConnected(std::string const& nsp) {
        std::cout << "Client connected" << std::endl;
    }

    void onDisconnected(std::string const& nsp) {
        std::cout << "Client disconnected" << std::endl;
    }

    void onFailed() {
        std::cout << "Connection failed" << std::endl;
    }
};

int main() {
    AudioServer server(5000); // Set your desired port
    server.run();

    return 0;
}
