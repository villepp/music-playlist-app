<template>
  <div id="app">
    <!-- Video Input Form -->
    <div>
      <input type="text" v-model="newVideo.url" placeholder="Video URL" />
      <input type="text" v-model="newVideo.title" placeholder="Video Title" />
      <VideoPlaylistComponent
    :videos="videos"
    @select-video="selectVideo"
  />
      <button @click="addVideo">Add Video</button>
    </div>

    <!-- Video Player -->
    <CustomYoutubePlayer
      ref="youtube"
      :autoplay="1"
      :videoid="currentVideoId"
      :loop="1"
      :controls="1"
    />

    <!-- Video Playlist -->
    <div class="playlist">
      <ul>
        <li v-for="video in videos" :key="video.id" @click="selectVideo(video)">
          {{ video.title }}
          <button @click="deleteVideo(video.id)">Delete</button>
        </li>
      </ul>
    </div>
  </div>
</template>
<script>
import axios from 'axios';
import CustomYoutubePlayer from "@/components/CustomYoutubePlayer";
// import VideoPlaylistComponent from "@/components/VideoPlaylistComponent";

export default {
  name: "App",
  components: {
    CustomYoutubePlayer,
  },
  data() {
    return {
      videos: [],
      currentVideoId: null,
      newVideo: { url: "", title: "" },
    };
  },
  created() {
    this.fetchVideos();
  },
  methods: {
    fetchVideos() {
      axios.get('http://localhost:5000/api/videos')
        .then(response => {
          this.videos = response.data;
          if (this.videos.length > 0) {
            this.currentVideoId = this.extractVideoId(this.videos[0].url);
          }
        })
        .catch(error => console.error('Error fetching videos:', error));
    },
    addVideo() {
      axios.post('http://localhost:5000/api/videos', this.newVideo)
        .then(response => {
          this.videos.push(response.data);
          this.newVideo = { url: "", title: "" };
        })
        .catch(error => console.error('Error adding video:', error));
    },
    deleteVideo(id) {
      axios.delete(`http://localhost:5000/api/videos/${id}`)
        .then(() => {
          this.videos = this.videos.filter(video => video.id !== id);
        })
        .catch(error => console.error('Error deleting video:', error));
    },
    selectVideo(video) {
      this.currentVideoId = this.extractVideoId(video.url);
    },
    extractVideoId(url) {
      const match = url.match(/(?:https?:\/\/)?(?:www\.)?(?:youtube\.com\/(?:[^/\n\s]+\/\S+\/|(?:v|e(?:mbed)?)\/|\S*?[?&]v=)|youtu\.be\/)([a-zA-Z0-9_-]{11})/);
      return match ? match[1] : null;
    },
  },
};
</script>

<style>
/* Add styles for your app here */
</style>