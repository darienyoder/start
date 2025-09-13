async function load_feeds()
{
    try
    {
        const feeds = [
            ["News", "https://feeds.nbcnews.com/nbcnews/public/news"],
            ["Jobs", "https://remote.co/feed"],
        ];

        const feed_list = [];
        let key = 0;
        for (var feed of feeds)
        {
            key += 1;
            feed_list.push(<Feed key={key} title={feed[0]} link={feed[1]} />)
        }
    
        const container = document.getElementById('feeds');
        const root = ReactDOM.createRoot(container);
        root.render(feed_list);
    }
    catch (error)
    {
        console.error(error.message);
    }
}

function Entry({title, content, link})
{
    return (
        <div>
            <a href={link}>{title}</a>
        </div>
    );
}

async function Feed({title, link})
{
    const response = await fetch(link);
    if (!response.ok)
    {
        throw new Error(`Response status: ${response.status}`);
    }

    const parser = new DOMParser();
    const xmlDoc = parser.parseFromString(response.text, 'text/xml');

    const entries = [];
    let key = 0;
    for (item of xmlDoc.getElementsByTagName('item'))
    {
        key += 1;
        entries.push( <Entry key={key} title={item.title} content="" link="" /> )
    }
    return (
        <div className="feed">
            {entries}
        </div>
    );
}

load_feeds();
