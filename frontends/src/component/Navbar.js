import React, { Component } from 'react';
import { Navbar, Nav, NavDropdown } from 'react-bootstrap';
import 'antd/dist/antd.css';
import { Modal,Button} from 'antd';
import LoginModal from './Account/LoginModal';



class NavBar extends Component {

    constructor(props) {
        super(props);
        this.state = {
            loading: false,
            visible: false,
        }
        this.showModal = this.showModal.bind(this);
        


    }

    showModal () {
        this.setState( {
            visible: true,
        })
    }
    
    handleOk = () => {
        this.setState({ loading: true });
        setTimeout(() => {
          this.setState({ loading: false, visible: false });
        }, 3000);
      };


    handleCancel = () => {
        this.setState({ visible: false });
      };

    render() {
 

        return (
           
            <Navbar collapseOnSelect expand="lg" bg="dark" variant="dark">
            <Navbar.Brand href="/">React-Bootstrap</Navbar.Brand>
            <Navbar.Toggle aria-controls="responsive-navbar-nav" />
            <Navbar.Collapse id="responsive-navbar-nav">
                <Nav className="mr-auto">
                <Nav.Link href="/info">정보게시판</Nav.Link>
                <Nav.Link href="/community">자유게시판</Nav.Link>
                <Nav.Link href="/selftrain">ai운동하기</Nav.Link>
                <Nav.Link href="/videoclass">유료강의</Nav.Link>
                <NavDropdown title="Dropdown" id="collasible-nav-dropdown">
                    <NavDropdown.Item href="#action/3.1">Action</NavDropdown.Item>
                    <NavDropdown.Item href="#action/3.2">Another action</NavDropdown.Item>
                    <NavDropdown.Item href="#action/3.3">Something</NavDropdown.Item>
                    <NavDropdown.Divider />
                    <NavDropdown.Item href="#action/3.4">Separated link</NavDropdown.Item>
                </NavDropdown>
                </Nav>
                <Nav>
                <Nav.Link onClick={this.showModal}>로그인</Nav.Link>
                <Modal
                    visible={this.state.visible}
                    title="로그인 하시겠습니까?"
                    onOk={this.handleOk}
                    onCancel={this.handleCancel}
                    footer={[
                    
                        <Button key="submit" type="primary" onClick={this.handleOk}>
                          로그인
                        </Button>,
                      ]}
                    >
                        <LoginModal/>
                    </Modal>
                
                <Nav.Link eventKey={2} href="#">
                    로그아웃
                </Nav.Link>
                <Nav.Link href="/signup">
                      회원가입
                </Nav.Link>
                </Nav>
            </Navbar.Collapse>
            </Navbar>
        )
    }
}

export default NavBar