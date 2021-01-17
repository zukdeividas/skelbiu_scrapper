import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { makeStyles } from '@material-ui/core/styles';
import { DataGrid } from '@material-ui/data-grid';
import ItemActionButtons from '../../Components/ItemActionButtons/ItemActionButtons';

const useStyles = makeStyles((theme) => ({
  root: {
    paddingTop: 50,
    flexGrow: 1,
    width: '100%',
  },
  dataGrid: {
    marginBottom: 50,
    width: '100%',
    boxShadow: '1px 4px 7px #9E9E9E',
  },
}));

export default function PostsTable() {
  const classes = useStyles();

  const [posts, setPosts] = useState();

  const columns = [
    { field: 'price', headerName: 'Price', width: 150 },
    { field: 'house_area', headerName: 'House area', width: 150 },
    { field: 'land_area', headerName: 'Land area', width: 150 },
    {
      field: 'id',
      headerName: 'Options',
      renderCell: (params) => (
        <ItemActionButtons
          data={params.row}
          liked={() => handlePostLike(params.row.id)}
          seen={() => handlePostSeen(params.row.id)}
          isDataTable={true}
        />
      ),
      width: 300,
    },
  ];

  const retrievePosts = () => {
    const params = new URLSearchParams([
      ['is_liked', 0],
      ['is_new', 0],
    ]);
    return axios.get('http://localhost:5000/api/posts', { params });
  };

  useEffect(() => {
    updatePosts();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const updatePosts = () => {
    retrievePosts().then((res) => {
      console.log(res.data);
      setPosts(res.data);
    });
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

  return (
    <div className={classes.root}>
      {posts ? (
        <DataGrid
          className={classes.dataGrid}
          autoHeight
          rows={posts}
          columns={columns}
          pageSize={13}
          rowsPerPageOptions={[13, 20, 30]}
          pagination
          disableMultipleSelection
        />
      ) : (
        'Loading...'
      )}
    </div>
  );
}
