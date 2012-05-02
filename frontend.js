var http = require('http'),
    httpProxy = require('http-proxy');

var options = {
  router: {
	"localhost/e": "127.0.0.1:9001",
	".*": "127.0.0.1:8000"
  }
};
var proxyServer = httpProxy.createServer(options);
proxyServer.listen(8081);
