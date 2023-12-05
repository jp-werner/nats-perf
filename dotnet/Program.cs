using Microsoft.Extensions.Logging;
using NATS.Client.Core;
using NATS.Client.JetStream;
using NATS.Client.ObjectStore;



Console.WriteLine("Hello nats-perf");

const string obs_bucket = "dotnet_bucket";

await using var nats = new NatsConnection();
var js = new NatsJSContext(nats);

var obj = new NatsObjContext(js);
var store = await obj.CreateObjectStore(obs_bucket);

while (true)
{
    try
    {
        await store.PutAsync(
            "wochendaemmerung.opus",
            File.OpenRead("/Users/jan.werner/Downloads/wochendaemmerung.opus")
        );
    }
    catch (Exception ex)
    {
        // Custom error handling or logging
        Console.WriteLine("An error occurred while calling PutAsync: " + ex.Message);
    }
}