import React, { useState, useEffect } from 'react';
import axios from 'axios';
import PostItem from './PostItem/PostItem';
import { Checkbox, FormControlLabel, Grid } from '@material-ui/core';
import { makeStyles } from '@material-ui/core/styles';

const useStyles = makeStyles((theme) => ({
  root: {
    paddingTop: 50,
    flexGrow: 1,
  },
}));

export default function PostsPreview() {
  const [posts, setPosts] = useState();
  const [likedFilter, setLikedFilter] = useState(false);
  const [newFilter, setNewFilter] = useState(false);

  const classes = useStyles();

  const retrievePosts = () => {
    const params = new URLSearchParams([
      ['is_liked', likedFilter],
      ['is_new', newFilter],
    ]);

    return axios.get('http://localhost:5000/api/posts', { params });
  };

  useEffect(() => {
    updatePosts();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  useEffect(() => {
    updatePosts();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [newFilter, likedFilter]);

  const updatePosts = () => {
    retrievePosts().then((res) => {
      setPosts(res.data);
    });
  };

  const handleLikedCheckboxChange = (event) => {
    setLikedFilter(event.target.checked);
  };

  const handleIsNewCheckboxChange = (event) => {
    setNewFilter(event.target.checked);
  };

  const handlePostLike = (postId) => {
    axios
      .get('http://localhost:5000/api/posts/' + postId + '/liked')
      .then(() => {
        const newList = posts.map((item) => {
          if (item.id === postId) item.is_liked = !item.is_liked;
          return item;
        });
        setPosts(newList);
      });
  };

  const handlePostSeen = (postId) => {
    axios
      .get('http://localhost:5000/api/posts/' + postId + '/seen')
      .then(() => {
        const newList = posts.map((item) => {
          if (item.id === postId) item.is_new = false;
          return item;
        });
        setPosts(newList);
      });
  };

  const listItems = posts
    ? posts.map((post) => (
        <Grid item key={post.id}>
          <PostItem
            data={post}
            liked={() => handlePostLike(post.id)}
            seen={() => handlePostSeen(post.id)}
          />
        </Grid>
      ))
    : 'Loading...';

  return (
    <div className={classes.root}>
      <FormControlLabel
        value="end"
        control={
          <Checkbox
            checked={likedFilter}
            onChange={handleLikedCheckboxChange}
            name="Liked"
            color="primary"
          />
        }
        label="Filter liked posts"
      />
      <FormControlLabel
        value="end"
        control={
          <Checkbox
            checked={newFilter}
            onChange={handleIsNewCheckboxChange}
            name="New"
            color="primary"
          />
        }
        label="Filter new posts"
      />

      <Grid container spacing={2} justify="center">
        {listItems}
      </Grid>
    </div>
  );
}
