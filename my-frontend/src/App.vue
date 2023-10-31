<template>
  <div id="app">
    <div class="video-player">
      <iframe ref="youtubeIframe" v-if="currentVideo"
        :src="`https://www.youtube.com/embed/${extractVideoId(currentVideo.url)}?autoplay=1`" frameborder="0"
        allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
        allowfullscreen></iframe>
    </div>
    <div class="controls">
      <button @click="previousVideo">Previous</button>
      <button v-if="!playing" @click="playVideo">Play</button>
      <button v-else @click="pauseVideo">Pause</button>
      <button @click="nextVideo">Next</button>
    </div>
    <ul class="playlist">
      <li v-for="video in videos" :key="video.id" @click="selectVideo(video)">
        {{ video.title }}
      </li>
    </ul>
  </div>
</template>

<script>
/* global YT */
import axios from 'axios';

export default {
  data() {
    return {
      videos: [],
      currentVideo: null,
      playing: false,
      player: null
    };
  },
  mounted() {
    this.getVideos();
    window.onYouTubeIframeAPIReady = () => {
      this.player = new YT.Player('player', {
        height: '390',
        width: '640',
        videoId: this.extractVideoId(this.currentVideo.url),
        events: {
          'onReady': this.onPlayerReady,
          'onStateChange': this.onPlayerStateChange
        }
      });
    };

  },
  beforeUnmount() {
    if (this.player) {
      this.player.destroy();
      this.player = null;
    }
  },
  methods: {
    async getVideos() {
      try {
        const response = await axios.get('http://localhost:5000/api/videos');
        this.videos = response.data;
        if (this.videos.length > 0) {
          this.currentVideo = this.videos[0];
        }
      } catch (error) {
        console.error('An error occurred!', error);
      }
    },
    createPlayer() {
      if (this.$refs.youtubeIframe && YT) {
        this.player = new YT.Player(this.$refs.youtubeIframe, {
          events: {
            'onReady': this.onPlayerReady,
          }
        });
      }
    },
    onPlayerReady() {
      this.playVideo();
      this.playing = true;
    },

    playVideo() {
      if (this.player) {
        this.player.playVideo();
      }
      this.playing = true;
    },
    pauseVideo() {
      if (this.player) {
        this.player.pauseVideo();
      }
      this.playing = false;
    },
    nextVideo() {
      const currentIndex = this.videos.findIndex(v => v.id === this.currentVideo.id);
      if (currentIndex < this.videos.length - 1) {
        this.currentVideo = this.videos[currentIndex + 1];
      }
    },
    previousVideo() {
      const currentIndex = this.videos.findIndex(v => v.id === this.currentVideo.id);
      if (currentIndex > 0) {
        this.currentVideo = this.videos[currentIndex - 1];
      }
    },
    selectVideo(video) {
      this.currentVideo = video;
    },
    extractVideoId(url) {
      const match = url.match(/(?:https?:\/\/)?(?:www\.)?(?:youtube\.com\/(?:[^/\n\s]+\/\S+\/|(?:v|e(?:mbed)?)\/|\S*?[?&]v=)|youtu\.be\/)([a-zA-Z0-9_-]{11})/);
      return match ? match[1] : null;
    }
  }
};
</script>

<style>
#app {
  text-align: center;
  margin-top: 60px;
}

.video-player {
  width: 300px;
  height: 150px;
  margin: 0 auto 20px;
}

.controls {
  margin-bottom: 20px;
}

.playlist {
  list-style-type: none;
  padding: 0;
}

.playlist li {
  cursor: pointer;
  padding: 10px;
  border: 1px solid #ccc;
  margin-top: -1px;
  background-color: #f9f9f9;
}

.playlist li:hover {
  background-color: #f1f1f1;
}
</style>
