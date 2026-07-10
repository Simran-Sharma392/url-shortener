const shortenBtn = document.getElementById("shortenBtn");
const result = document.getElementById("result");
const copyBtn = document.getElementById("copyBtn");
const statsBtn = document.getElementById("statsBtn");
const statsResult = document.getElementById("statsResult");
const updateBtn = document.getElementById("updateBtn");
const updateResult = document.getElementById("updateResult");
const deleteBtn = document.getElementById("deleteBtn");
const deleteResult = document.getElementById("deleteResult");

let shortUrl="";

shortenBtn.addEventListener("click", async()=>{
    const url=document.getElementById("url").value.trim();
    const slug=document.getElementById("slug").value.trim();

    if(!url){
        alert("Please enter a URL.");
        return;
    }

    const body={
        url: url
    };

    if(slug){
        body.slug=slug;
    }

    try{
        const response= await fetch("/shorten", {
            method: "POST",
            headers:{
                "Content-Type": "application/json"
            },
            body: JSON.stringify(body)
        });

        const data=await response.json();

        if(!response.ok){
        const message = Array.isArray(data.detail)
            ? data.detail[0].msg
            : data.detail;

        result.innerHTML = `<p style="color:red;">${message}</p>`;
        return;       
        }

        shortUrl = `${window.location.origin}/${data.shortCode}`;

        result.innerHTML = `
        <h3>Short URL Created 🎉</h3>
        <p>
            <a href="${shortUrl}" target="_blank">
                ${shortUrl}
            </a>
        </p>`;
        copyBtn.style.display = "block";
    } catch(error){
        result.innerHTML=` <p style="color:red;">Something went wrong.</p>`;
    }
});

copyBtn.addEventListener("click", async()=>{
    await navigator.clipboard.writeText(shortUrl);
    copyBtn.textContent="Copied!";
    setTimeout(()=>{
        copyBtn.textContent = "Copy Short URL"
    }, 1500);

});

statsBtn.addEventListener("click", async () => {

    const slug = document.getElementById("statsSlug").value.trim();

    if (!slug) {
        alert("Enter a short code.");
        return;
    }

    const response = await fetch(`/shorten/${slug}/stats`);

    const data = await response.json();

    if (!response.ok) {
        statsResult.innerHTML = `<p style="color:red;">${data.detail}</p>`;
        return;
    }

    statsResult.innerHTML = `
        <h3>Statistics</h3>

        <p><strong>Original URL:</strong> ${data.url}</p>

        <p><strong>Short Code:</strong> ${data.shortCode}</p>

        <p><strong>Total Clicks:</strong> ${data.accessCount}</p>

        <p><strong>Total Records:</strong> ${data.clicks.length}</p>
    `;

});

updateBtn.addEventListener("click", async () => {

    const slug = document.getElementById("updateSlug").value.trim();
    const url = document.getElementById("newUrl").value.trim();

    if (!slug || !url) {
        alert("Fill all fields.");
        return;
    }

    const response = await fetch(`/shorten/${slug}`, {
        method: "PUT",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            url: url
        })
    });

    const data = await response.json();

    if (!response.ok) {
        updateResult.innerHTML = `<p style="color:red;">${data.detail}</p>`;
        return;
    }

    updateResult.innerHTML =
        `<p style="color:green;">URL updated successfully ✅</p>`;

});

deleteBtn.addEventListener("click", async () => {

    const slug = document.getElementById("deleteSlug").value.trim();

    if (!slug) {
        alert("Enter a short code.");
        return;
    }

    const response = await fetch(`/shorten/${slug}`, {
        method: "DELETE"
    });

    if (response.status === 204) {
        deleteResult.innerHTML =
            `<p style="color:green;">URL deleted successfully ✅</p>`;
        return;
    }

    const data = await response.json();

    deleteResult.innerHTML =
        `<p style="color:red;">${data.detail}</p>`;

});