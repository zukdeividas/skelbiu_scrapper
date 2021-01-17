import React from 'react';
import { makeStyles } from '@material-ui/core/styles';
import IconButton from '@material-ui/core/IconButton';
import FavoriteIcon from '@material-ui/icons/Favorite';
import Lightbox from 'react-image-lightbox';
import 'react-image-lightbox/style.css';
import {
  Description,
  NewReleases,
  OpenInBrowser,
  Photo,
  RemoveRedEye,
} from '@material-ui/icons';
import {
  Button,
  Dialog,
  DialogActions,
  DialogContent,
  DialogTitle,
  Typography,
} from '@material-ui/core';

const useStyles = makeStyles(() => ({
  root: {
    width: 250,
  },
}));

export default function ItemActionButtons(props) {
  const classes = useStyles();
  const [photoIndex, setPhotoIndex] = React.useState(0);
  const [isOpen, setIsOpen] = React.useState(false);
  const [showDescription, setShowDescription] = React.useState(false);

  const post = props.data;

  const imageClickHandler = () => {
    setIsOpen(true);
  };

  const showDescriptionHandler = () => {
    setShowDescription(true);
  };

  const closeDescriptionHandler = () => {
    setShowDescription(false);
  };

  const seenButton = post.is_new ? (
    <IconButton onClick={props.seen}>
      <NewReleases color="primary" />
    </IconButton>
  ) : (
    <IconButton>
      <RemoveRedEye />
    </IconButton>
  );

  return (
    <div className={classes.root}>
      <Dialog onClose={closeDescriptionHandler} open={showDescription}>
        <DialogTitle onClose={closeDescriptionHandler}>Description</DialogTitle>
        <DialogContent dividers>
          <Typography gutterBottom>{post.description}</Typography>
        </DialogContent>
        <DialogActions>
          <Button autoFocus onClick={closeDescriptionHandler} color="primary">
            Close
          </Button>
        </DialogActions>
      </Dialog>
      {isOpen && (
        <Lightbox
          mainSrc={post.image_urls[photoIndex]}
          nextSrc={post.image_urls[(photoIndex + 1) % post.image_urls.length]}
          prevSrc={
            post.image_urls[
              (photoIndex + post.image_urls.length - 1) % post.image_urls.length
            ]
          }
          onCloseRequest={() => setIsOpen(false)}
          onMovePrevRequest={() =>
            setPhotoIndex(
              (photoIndex + post.image_urls.length - 1) % post.image_urls.length
            )
          }
          onMoveNextRequest={() =>
            setPhotoIndex((photoIndex + 1) % post.image_urls.length)
          }
        />
      )}
      {props.isDataTable ? (
        <IconButton onClick={imageClickHandler}>
          <Photo color="primary" />
        </IconButton>
      ) : (
        ''
      )}

      <IconButton onClick={props.liked}>
        <FavoriteIcon color={post.is_liked ? 'primary' : 'action'} />
      </IconButton>

      {seenButton}

      <IconButton onClick={() => window.open(post.original_url, '_blank')}>
        <OpenInBrowser color="primary" />
      </IconButton>
      <IconButton onClick={showDescriptionHandler}>
        <Description color="primary" />
      </IconButton>
    </div>
  );
}
