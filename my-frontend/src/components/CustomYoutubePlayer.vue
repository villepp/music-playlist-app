<!-- components/CustomYoutubePlayer.vue -->
<template>
    <div class="video-player">
        <div ref="player" :id="playerId"></div>
        <div class="video-controls">
            <button @click="playVideo">Play</button>
            <button @click="stopVideo">Stop</button>
            <button @click="pauseVideo">Pause</button>
        </div>
    </div>
</template>
  
<script>
import YouTubePlayer from "youtube-player";
import shortid from "shortid";

export default {
    name: "CustomYoutubePlayer",
    props: {
        autoplay: { type: Number, default: 1 },
        videoid: { type: String, required: true },
        loop: { type: Number, default: 1 },
        controls: { type: Number, default: 1 },
        modestbranding: { type: Number, default: 1 },
    },
    data() {
        return {
            player: null,
            playerId: "youtube-player-" + shortid.generate(),
        };
    },
    mounted() {
        console.log("Player ID:", this.playerId);
        console.log("Player Element:", this.$refs.player);
        this.initializePlayer();
    },

    watch: {
        videoid(newVal) {
            this.player.loadVideoById(newVal);
        },
    },
    methods: {
        
    playVideo() {
        if (this.player) {
            this.player.playVideo();
        }
    },
    stopVideo() {
        if (this.player) {
            this.player.stopVideo();
        }
    },
    pauseVideo() {
        if (this.player) {
            this.player.pauseVideo();
        }
    },
        initializePlayer() {

            let playerVars = {
                autoplay: this.autoplay,
                loop: this.loop,
                controls: this.controls,
                modestbranding: this.modestbranding,
            };
            this.player = YouTubePlayer(this.playerId, {
                width: 640,
                height: 480,
                videoId: this.videoid,
                playerVars: playerVars,
            });
            this.player.on("stateChange", (e) => {
                if (e.data === window.YT.PlayerState.ENDED) this.$emit("ended");
                else if (e.data === window.YT.PlayerState.PAUSED) this.$emit("paused");
                else if (e.data === window.YT.PlayerState.PLAYING) this.$emit("played");
            });
        },
    },
    beforeUnmount() {
        if (this.player) this.player.destroy();
    },
};
</script>