import React, { useState } from 'react';
import FileCreate from './FileCreate';
import { useDispatch } from "react-redux";
import { createArticle } from "../../_actions/index";


function ArticleCreate(props) {
  const dispatch = useDispatch();

  const [Title, setTitle] = useState("")
  const [Description, setDescription] = useState("")
  const [Images, setImages] = useState([])

  const titleChangeHandler = (e) => {
    setTitle(e.currentTarget.value)
  }

  const descriptionChangeHandler = (e) => {
    setDescription(e.currentTarget.value)
  }

  const updateImages = (newImages) => {
    setImages(newImages)
  }

  const submitHandler = (e) => {
    e.preventDefault();

    if (!Title || !Description) {
        return alert("값을 입력해주셔야 합니다.")
    }

    //서버에 채운 값들을 request로 보낸다.

    const body = {
        //로그인 된 사람의 ID 
        // writer: props.user.userData._id,
        title: Title,
        content: Description,
        // images: Images
      }

      dispatch(createArticle(body))
      .then((res) => {
        props.history.push('/Community')
        console.log('1111111');
      });
      // Axios.post('/api/product', body)
      //       .then(response => {
      //           if (response.data.success) {
      //               alert('상품 업로드에 성공 했습니다.')
      //               props.history.push('/')
      //           } else {
      //               alert('상품 업로드에 실패 했습니다.')
      //           }
      //       })
          }


  return (
    <div className="ArticleCreate">
      <form onSubmit={submitHandler}>
        
        <label>Title</label>
        <input onChange={titleChangeHandler} value={Title}/>
        <br/>
        <label>Desc</label>
        <textarea onChange={descriptionChangeHandler} value={Description}/>
        <br/>
        <FileCreate refreshFunction={updateImages}/>
        <button type="submit">Submit</button>
      </form>
    </div>
  )
  }


export default ArticleCreate;