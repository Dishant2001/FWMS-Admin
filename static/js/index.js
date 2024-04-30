document.addEventListener("click", function(event) {
    // Check if the clicked element is a button
    console.log("clicked");
    if (event.target) {
        // Handle button click
        var id = event.target.id;
        handleClick(id);
        console.log(id+" clicked");
    }
});

async function handleClick(id){
    const resp = await fetch("http://127.0.0.1:5000/run-strategy/"+id);
    const data = await resp.json();
    console.log(data);
}