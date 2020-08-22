document.addEventListener("DOMContentLoaded", function () {
  document.querySelectorAll(".like_unlike").forEach((button) => {
    button.onclick = () => {
      let post = button.parentElement.parentElement;
      postid = post.dataset.postid;
      fetch(`/likeUnlike/${postid}`, {
        method: "POST",
      });
      if (button.dataset.liked === "true") {
        button.dataset.liked = "false";
        button.dataset.likes -= 1;
        button.style.backgroundColor = "blue";
        button.innerHTML = `Like: (${button.dataset.likes})`;
      } else {
        button.dataset.liked = "true";
        button.dataset.likes++;
        button.style.backgroundColor = "grey";
        button.innerHTML = `Unlike: (${button.dataset.likes})`;
      }
    };
  });
  document.querySelectorAll(".deleteButton").forEach((button) => {
    button.onclick = () => {
      let post = button.parentElement.parentElement;
      fetch(`/deletepost/${post.dataset.postid}`, {
        method: "POST",
      });
      post.innerHTML = "";
    };
  });

  document.querySelectorAll(".editButton").forEach((button) => {
    button.onclick = () => {
      let postId = button.parentElement.parentElement.dataset.postid;
      document.querySelector(`#editPost${postId}`).style.display = "block";
      document.querySelector(`#Post${postId}`).style.display = "none";
      document.querySelector(`#newPostSubmit-${postId}`).onclick = () => {
        newPostContentValue = document.querySelector(
          `#newPostTextArea-${postId}`
        ).value;
        fetch(`/edit/${postId}`, {
          method: "PUT",
          body: JSON.stringify({
            postcontent: newPostContentValue,
          }),
        });
        document.querySelector(`#editPost${postId}`).style.display = "none";
        document.querySelector(
          `#postContent-${postId}`
        ).innerHTML = newPostContentValue;
        document.querySelector(`#Post${postId}`).style.display = "block";
      };
    };
  });

  let followButton = document.querySelector("#followButton");
  if (followButton != null) {
    followButton.onclick = () => {
      console.log();
      status = followButton.innerHTML;
      if (status === "Follow") {
        followButton.innerHTML = "UnFollow";
        document.querySelector("#followerCount").innerHTML++;
      }
      if (status === "UnFollow") {
        followButton.innerHTML = "Follow";
        document.querySelector("#followerCount").innerHTML--;
      }
      fetch(`toggleFollow/${followButton.dataset.username}`, {
        method: "POST",
      });
    };
  }
});
