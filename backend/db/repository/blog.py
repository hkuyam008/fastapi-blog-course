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
    blog_in_db = retrieve_blog(id=id, db=db)
    if blog_in_db:
        blog_in_db.title = blog.title
        blog_in_db.content = blog.content
        
        db.add(blog_in_db)
        db.commit()
        
    return blog_in_db

def delete_blog_by_id(id: int, db: Session, author_id=1):
    blog_in_db = db.query(Blog).filter(Blog.id==id)
    
    if not blog_in_db.first():
        return {"error": f"Could not find blog with the id {id}"}
    
    blog_in_db.delete()
    db.commit()
    
    return {"msg": f"Deleted blog with id {id}"}