import React from 'react';
import { makeStyles } from '@material-ui/core/styles';
import Card from '@material-ui/core/Card';
import CardHeader from '@material-ui/core/CardHeader';
import CardMedia from '@material-ui/core/CardMedia';
import CardContent from '@material-ui/core/CardContent';
import CardActions from '@material-ui/core/CardActions';
import IconButton from '@material-ui/core/IconButton';
import Typography from '@material-ui/core/Typography';
import FavoriteIcon from '@material-ui/icons/Favorite';
import MoreVertIcon from '@material-ui/icons/MoreVert';
import Lightbox from 'react-image-lightbox';
import 'react-image-lightbox/style.css';
import {
  Description,
  NewReleases,
  OpenInBrowser,
  RemoveRedEye,
} from '@material-ui/icons';
import {
  Button,
  Dialog,
  DialogActions,
  DialogContent,
  DialogTitle,
} from '@material-ui/core';
import ItemActionButtons from '../../../Components/ItemActionButtons/ItemActionButtons';

const useStyles = makeStyles((theme) => ({
  root: {
    width: 250,
  },
  media: {
    height: 0,
    paddingTop: '56.25%', // 16:9
  },
  expand: {
    transform: 'rotate(0deg)',
    marginLeft: 'auto',
    transition: theme.transitions.create('transform', {
      duration: theme.transitions.duration.shortest,
    }),
  },
  expandOpen: {
    transform: 'rotate(180deg)',
  },
  headerTitle: {
    fontSize: 13,
  },
  contentText: {
    fontSize: 13,
  },
  cardContent: {
    textAlign: 'left',
  },
  description: {
    fontSize: 13,
  },
}));

export default function PostItem(props) {
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
    <Card className={classes.root}>
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
      <CardHeader
        action={
          <IconButton aria-label="settings">
            <MoreVertIcon />
          </IconButton>
        }
        subheader={
          <Typography className={classes.headerTitle}>
            {post.town + ' ' + post.street}
          </Typography>
        }
      />
      <CardMedia
        className={classes.media}
        image={post.image_urls[0]}
        onClick={imageClickHandler}
      />
      <CardContent className={classes.cardContent}>
        <Typography className={classes.contentText}>
          <b>Price:</b> {post.price} EUR
        </Typography>
        <Typography className={classes.contentText}>
          <b>Rooms:</b> {post.room_count}
        </Typography>
        <Typography className={classes.contentText}>
          <b>Year:</b> {post.year}
        </Typography>
        <Typography className={classes.contentText}>
          <b>Heating:</b> {post.heating}
        </Typography>
        <Typography className={classes.contentText}>
          <b>House area:</b> {post.house_area} m<sup>2</sup>
        </Typography>
        <Typography className={classes.contentText}>
          <b>Land area:</b> {post.land_area} a
        </Typography>
      </CardContent>
      <CardActions disableSpacing>
        <ItemActionButtons data={post} />
      </CardActions>
    </Card>
  );
}
