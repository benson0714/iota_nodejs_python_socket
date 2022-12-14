const { ClientBuilder } = require('@iota/client')

const index = 'Benson_dht11_test';
async function messages_send(index, data) {
    const client = new ClientBuilder()
        .node('http://127.0.0.1:14265')
        .build();
        // https:/domaim/IOTA_api_14265/
        // .node('https://api.lb-0.h.chrysalis-devnet.iota.cafe')
        // .build()
    // client.getInfo().then(console.log).catch(console.error)
    const message = await client.message()
            .index(index)
            .data(data)
            .submit();
    return message.messageId;
}




async function socket() {
    var net = require('net');

    var port = 15768;
    var host = '127.0.0.1';

    var server = net.createServer((socket) => {
        socket.on('data',async (data) => {
            console.log(`Server: Received ${data}`);
            const msgId = await messages_send(index, data);
            socket.write(msgId);
            socket.pipe(socket);
        });
        socket.on('end', () => {
            console.log('Server: Client Disconnected');
        });
    });
    server.on('connection', (socket) => {
        console.log(`Server: ${socket.remoteAddress}:${socket.remotePort} has connected`);
    });
    server.on('error', (err) => {
        throw err;
    });
    server.on('listening', () => {
        var address = server.address();
        console.log(`opened server on ${address.address}:${address.port}`);
    });
    server.listen(port, host);
}

async function run(){
    await socket();
}


run()