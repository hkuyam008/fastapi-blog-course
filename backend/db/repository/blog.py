from sqlalchemy.orm import Session
from schemas.blog import CreateBlog, UpdateBlog
from db.models.blog import Blog


def create_new_blog(blog: CreateBlog, db: Session, author_id: int):
    blog = Blog(
        title = blog.title,
        slug = blog.slug,
        content = blog.content,
        author_id = author_id,
        is_active = True
    )
    
    db.add(blog)
    db.commit()
    db.refresh(blog)
    
    return blog

def retrieve_blog(id: int, db: Session):
    return db.query(Blog).filter(Blog.id==id).first()

def list_blogs(db: Session):
    return db.query(Blog).filter(Blog.is_active==True)

def update_blog_by_id(id: int, blog: UpdateBlog, db: Session, author_id: int):
    
    blog_in_db = db.query(Blog).filter(Blog.id==id).first()
    
    if not blog_in_db:
        return {"error":f"Blog with id {id} does not exist"}
    if not blog_in_db.author_id == author_id:
        return {"error": "Only the author can modify the blog"}
    
    blog_in_db.title = blog.title
    blog_in_db.content = blog.content
    
    db.add(blog_in_db)
    db.commit()
        
    return blog_in_db

def delete_blog_by_id(id: int, db: Session, author_id: int):
    blog_in_db = db.query(Blog).filter(Blog.id==id)
    
    if not blog_in_db.first():
        return {"error": f"Could not find blog with the id {id}"}
    if not blog_in_db.first().author_id == author_id:
        return {"error": "Only the author can delete the blog"}
    
    blog_in_db.delete()
    db.commit()
    
    return {"msg": f"Deleted blog with id {id}"}